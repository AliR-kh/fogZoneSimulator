from utilize.Algorithms.DRL.Scheduling.Fogs.env import Engine
import random
import torch
import torch.nn as nn
from torch.distributions import Categorical
import torch.nn.functional as F
import random
import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path
import csv

# یک ساختمان داده برای ذخیره تجربیات
# ==================== ابرپارامترها ====================
# ==================== Hyperparameters (Optimized for Task Scheduling) ====================

# (بدون تغییر) ضریب تنزیل برای پاداش‌های آینده
GAMMA = 0.95
# (بدون تغییر) پارامتر GAE برای تعادل بایاس و واریانس
LAMBDA = 0.90
# (تغییر) نرخ یادگیری کمی بالاتر برای همگرایی سریع‌تر. 3e-4 یک مقدار استاندارد و قوی برای PPO است.
LR = 5e-5
# (تغییر) تعداد دوره‌ها را کمی افزایش می‌دهیم تا از هر بچ داده، بیشتر یاد بگیریم.
K_EPOCHS = 20
# (بدون تغییر) ضریب برش برای تضمین آپدیت‌های پایدار
EPS_CLIP = 0.35
# (مهم‌ترین تغییر) این عدد را به طور قابل توجهی افزایش می‌دهیم تا داده‌های متنوع‌تری از چندین اپیزود جمع‌آوری شود.
UPDATE_INTERVAL = 1024
# (بدون تغییر) تعداد کل اپیزودهای آموزش
NUM_EPISODES = 300
# (بدون تغییر) این پارامترها مربوط به مشخصات محیط شما هستند.
STATE_SIZE = 5
ACTION_SIZE = 5
# NUM_TASKS = 200
# (بدون تغییر) این اندازه بچ برای بازه آپدیت جدید، مناسب است (2048 / 64 = 32).
BATCH_SIZE = 64
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class ActorCritic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )
        
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def act(self, state):
        # این متد برای جمع‌آوری داده است و نیازی به محاسبه گرادیان ندارد.
        with torch.no_grad():
            action_logits = self.actor(state)
            dist = Categorical(logits=action_logits)
            action = dist.sample()
            action_logprob = dist.log_prob(action)
        
        return action.detach(), action_logprob.detach()

    def evaluate(self, state, action):
        # رفع باگ حیاتی: حذف torch.no_grad() از اینجا.
        # این متد در حلقه آموزش استفاده می‌شود و باید گرادیان‌ها را محاسبه کند.
        # بدون این تغییر، هیچ یادگیری‌ای اتفاق نمی‌افتد.
        action_logits = self.actor(state)
        dist = Categorical(logits=action_logits)
        
        action_logprobs = dist.log_prob(action)
        dist_entropy = dist.entropy()
        state_value = self.critic(state)
        
        return action_logprobs, dist_entropy, state_value

# ساختار حافظه شما بدون تغییر باقی مانده است.
class Memory():
    def __init__(self):
        self.experiences=[]
        self.shuffle_experiences=[]

    def shuffle(self, number):
        random.shuffle(self.experiences)
        i=0
        while i < len(self.experiences):
            batches=[]
            self.shuffle_experiences=[]
            batches=self.experiences[i:i+number]
            self.shuffle_experiences.append(batches)
            i+=number

    def append(self, experience):
        self.experiences.append(experience)
        
    def len(self):
        return len(self.experiences)

    def clear(self):
        self.experiences=[]
        self.shuffle_experiences=[]

class RunFogScheduling_PPO():
    def __init__(self,resources,tasks):
        self.Env = Engine(resources=resources,tasks=tasks)
        self.actor_critic=ActorCritic(STATE_SIZE,ACTION_SIZE).to(device)
        self.actor_critic_old=ActorCritic(STATE_SIZE,ACTION_SIZE).to(device)
        # در ابتدا، وزن‌های هر دو شبکه یکسان هستند.
        self.actor_critic_old.load_state_dict(self.actor_critic.state_dict())
        self.losses=[]
        self.episode_scores=[]
        
        self.memory=Memory()
        
        # بهینه‌ساز اکنون تمام پارامترهای شبکه اصلی را بهینه می‌کند.
        self.optimizer=torch.optim.Adam(self.actor_critic.parameters(), lr=LR)
        
    def _train(self):
        # رفع باگ حیاتی: محاسبه صحیح GAE (تخمین مزیت تعمیم‌یافته)
        # این بخش باید قبل از بُر زدن و بچ‌بندی انجام شود.
        # ما به صورت عقب‌گرد در تجربیات حرکت می‌کنیم تا مزیت هر گام را محاسبه کنیم.
        advantage = 0
        # ما به مقادیر V(s_t) و V(s_{t+1}) نیاز داریم، بنابراین از حلقه for معکوس استفاده می‌کنیم.
        for i in reversed(range(len(self.memory.experiences))):
            exp = self.memory.experiences[i]
    
            # اگر آخرین تجربه باشد، ارزش حالت بعدی صفر است.
            is_last_experience = (i == len(self.memory.experiences) - 1)
            v_next = 0 if is_last_experience else self.memory.experiences[i+1]['V_t']
            
            # اگر حالت پایانی باشد، ارزش حالت بعدی صفر است.
            v_next = v_next * (1 - exp['done'])

            # محاسبه خطای TD (Temporal Difference)
            delta = exp['reward'] + (GAMMA * v_next) - exp['V_t']
            
            # محاسبه مزیت با استفاده از فرمول GAE
            advantage = delta + (GAMMA * LAMBDA * advantage * (1 - exp['done']))
            
            
            # محاسبه بازده (Return) که هدف شبکه منتقد است.
            G_t = advantage + exp['V_t']
            
            # ذخیره مقادیر محاسبه‌شده در حافظه
            self.memory.experiences[i]['A_t'] = advantage
            self.memory.experiences[i]['G_t'] = G_t
        # رفع باگ منطقی: حلقه Epochs
        # ما باید K_EPOCHS بار روی کل داده‌ها آموزش ببینیم.
        for _ in range(K_EPOCHS):
            total_loss = 0
            # در هر Epoch، داده‌ها را بُر زده و به مینی‌بچ‌هایی با اندازه BATCH_SIZE تقسیم می‌کنیم.
            self.memory.shuffle(BATCH_SIZE)
            for batch_experiences in self.memory.shuffle_experiences:
                # تبدیل لیست دیکشنری‌ها به دیکشنری تنسورها برای پردازش دسته‌ای
                states = torch.stack([exp['state'] for exp in batch_experiences]).to(device)
                actions = torch.stack([exp['action'] for exp in batch_experiences]).to(device)
                old_logprobs = torch.stack([exp['action_logprob'] for exp in batch_experiences]).to(device)
                
                # استخراج مزیت‌ها و بازده‌های محاسبه‌شده
                advantages = torch.stack([exp['A_t'] for exp in batch_experiences]).to(device)
                returns = torch.stack([exp['G_t'] for exp in batch_experiences]).to(device)

                # بهترین رویه: نرمال‌سازی مزیت‌ها برای پایداری آموزش
                advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
                
                # ارزیابی مجدد اقدامات با شبکه جدید
                logprobs, dist_entropy, state_values = self.actor_critic.evaluate(states, actions)
                
                # محاسبه نسبت خط‌مشی
                ratios = torch.exp(logprobs - old_logprobs.detach())
                
                # محاسبه زیان بازیگر (Actor Loss) با هدف جایگزین برش‌خورده PPO
                surr1 = ratios * advantages
                surr2 = torch.clamp(ratios, 1 - EPS_CLIP, 1 + EPS_CLIP) * advantages
                actor_loss = -torch.min(surr1, surr2).mean()
                
                # رفع باگ حیاتی: محاسبه زیان منتقد (Critic Loss)
                # هدف شبکه منتقد، پیش‌بینی بازده‌های محاسبه‌شده (G_t) است، نه ارزش قدیمی (V_t).
                critic_loss = F.mse_loss(state_values.squeeze(), returns)
                
                # زیان کل
                loss = actor_loss + 0.5 * critic_loss - 0.05 * dist_entropy.mean()
                
                # به‌روزرسانی وزن‌ها
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                total_loss += loss.mean().item()
                avg_loss = total_loss / K_EPOCHS
        self.losses.append(avg_loss)
        # رفع باگ حیاتی: به‌روزرسانی شبکه قدیمی با وزن‌های شبکه جدید
        # خطای تایپی self.policy به self.actor_critic اصلاح شد.
        self.actor_critic_old.load_state_dict(self.actor_critic.state_dict())
        
        # پاک کردن حافظه برای دور بعدی جمع‌آوری داده
        self.memory.clear()
        
    def _explore(self):
        # این متغیر برای کنترل زمان به‌روزرسانی استفاده می‌شود.
        timesteps_collected = 0
        for epoch in tqdm(range(NUM_EPISODES)):
            total_reward=0
            self.Env.reset()
            for task_index in range(self.Env.get_number_of_task()):
                timesteps_collected += 1
                
                # تبدیل وضعیت به تنسور
                temporary_state = torch.from_numpy(self.Env.temporary_state(task_index)).float().to(device)
                
                # عمل در محیط با استفاده از شبکه قدیمی (old_policy)
                action, action_logprob = self.actor_critic_old.act(temporary_state)
                
                # تخمین ارزش وضعیت با استفاده از منتقد قدیمی
                with torch.no_grad():
                    V_t = self.actor_critic_old.critic(temporary_state).squeeze()

                action_to_env = action.cpu().numpy()
                # فرض می‌شود که old_state و new_state در این پیاده‌سازی استفاده نمی‌شوند.
                old_state, new_state, reward, done = self.Env.step(task_index, action_to_env)
                total_reward += reward
                # ذخیره تجربه در حافظه
                self.memory.append({
                    "state": temporary_state,
                    "action": action,
                    "action_logprob": action_logprob,
                    "V_t": V_t,
                    "reward": torch.tensor(reward, dtype=torch.float32).to(device),
                    "done": torch.tensor(done, dtype=torch.float32).to(device)
                })
                
                # اگر داده کافی جمع‌آوری شد، آموزش را شروع کن.
                if timesteps_collected % UPDATE_INTERVAL == 0:
                    self._train()
                    # پس از آموزش، شمارنده را صفر می‌کنیم چون حافظه پاک شده است.
                    timesteps_collected = 0
            self.episode_scores.append(total_reward)
        CURRENT_PATH=Path(__file__).resolve().parent
        MODEL_PATH = CURRENT_PATH/'ppo_scheduler_model.pth'
        torch.save(self.actor_critic.state_dict(), MODEL_PATH)
    def _test(self):
        actions=[]
        CURRENT_PATH=Path(__file__).resolve().parent
        MODEL_PATH = CURRENT_PATH/'ppo_scheduler_model.pth' # مسیر فایل ذخیره شده
        try:
            self.actor_critic_old.load_state_dict(torch.load(MODEL_PATH))
            self.actor_critic_old.eval()
        # print(f"مدل با موفقیت از مسیر '{MODEL_PATH}' بارگذاری شد.")
        except FileNotFoundError:
        # print(f"خطا: فایل مدل در مسیر '{MODEL_PATH}' پیدا نشد. لطفاً ابتدا مدل را آموزش و ذخیره کنید.")
            exit()
        for task_index in range(self.Env.get_number_of_task()):
            temporary_state = torch.from_numpy(self.Env.temporary_state(task_index)).float().to(device)  
                # عمل در محیط با استفاده از شبکه قدیمی (old_policy)
            action, _ = self.actor_critic_old.act(temporary_state)
            action_to_env = action.cpu().numpy()
            actions.append(action_to_env.item())
            _, _, _, done = self.Env.step(task_index, action_to_env)
            if done:
                break

        # print(f"Final test reward is: {actions}")
        return actions
    
    def _plpt(self):
        with open("scheduling_loss.csv","w",newline="") as f:
            writer=csv.writer(f)
            for value in self.losses:
                writer.writerow([value])
                
        with open("scheduling_reward.csv","w",newline="") as f:
            writer=csv.writer(f)
            for value in self.episode_scores:
                writer.writerow([value])
        
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(self.episode_scores, label='Reward')
        plt.title('Episode Reward over Time')
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        plt.legend()
        plt.grid()

        plt.subplot(1, 2, 2)
        plt.plot(self.losses, label='Loss', color='red')
        plt.title('Training Loss over Time')
        plt.xlabel('Training Steps')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()
    def run(self):
        self._explore()
        self._plpt()
        # self._test()
