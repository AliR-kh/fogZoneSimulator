from utilize.Algorithms.DRL.Scheduling.Fogs.env import Engine
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import math
from collections import namedtuple, deque
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path

# یک ساختمان داده برای ذخیره تجربیات
Experience = namedtuple('Experience', ('state', 'action', 'reward', 'next_state', 'done'))

class ReplayBuffer:
    """بافر برای ذخیره و بازیابی تجربیات جهت آموزش"""
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """یک تجربه را ذخیره می‌کند"""
        self.memory.append(Experience(*args))

    def sample(self, batch_size):
        """یک دسته تصادفی از تجربیات را برمی‌گرداند"""
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size, seed=42):
        super(QNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, action_size)
        self.dropout = nn.Dropout(p=0.1)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = self.dropout(F.relu(self.fc2(x)))
        x = F.relu(self.fc3(x))
        return self.fc4(x)

class RunFogScheduling():
    def __init__(self,resources,tasks):        
        # هایپرپارامترهای DQN
        self.BATCH_SIZE = 128            # بزرگ‌تر از حالت قبلی برای نمونه‌گیری پایدارتر
        self.GAMMA = 0.95                # تنزیل ملایم برای توجه به آینده ولی با تمرکز بر حال
        self.EPS_START = 1.0             # اکتشاف کامل در ابتدا (100٪ اکشن تصادفی)
        self.EPS_END = 0.05              # در پایان 5٪ رفتار تصادفی حفظ میشه
        self.EPS_DECAY = 5000            # آهسته‌تر شدن روند کاهش اکتشاف برای کاهش bias
        self.TARGET_UPDATE = 500         # به‌روزرسانی مکررتر شبکه هدف برای سازگاری بهتر
        self.LR = 1e-6                   # نرخ یادگیری معقول برای شبکه کوچک تا متوسط
        self.NUM_EPISODES = 1000         # اپیزودهای بیشتر برای پوشش بیشتر وضعیت‌ها
        self.NUM_TASKS = 200              # بسته به اندازه مسئله‌ات خوبه
        self.STATE_SIZE = 5              # فرض بر اینکه 5 ویژگی مهم در state داری
        self.ACTION_SIZE = 5
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # ساختن شبکه‌ها، بهینه‌ساز و بافر
        self.policy_net = QNetwork(self.STATE_SIZE, self.ACTION_SIZE).to(self.device)
        self.target_net = QNetwork(self.STATE_SIZE, self.ACTION_SIZE).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.LR)
        self.memory = ReplayBuffer(1000000)
        self.steps_done = 0
        self.env = Engine(resources=resources,tasks=tasks)
    # ==============================================================================
    # ۲. توابع کمکی برای انتخاب اقدام و بهینه‌سازی
    # ==============================================================================

    def select_action(self,state):
        """انتخاب اقدام بر اساس سیاست اپسیلون-حریصانه"""
        sample = random.random()
        eps_threshold = self.EPS_END + (self.EPS_START - self.EPS_END) * math.exp(-1. * self.steps_done / self.EPS_DECAY)
        self.steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                # از شبکه اصلی برای انتخاب بهترین اقدام استفاده کن
                return self.policy_net(state).max(1)[1].view(1, 1)
        else:
            # یک اقدام تصادفی انتخاب کن
            return torch.tensor([[random.randrange(self.ACTION_SIZE)]], device=self.device, dtype=torch.long)

    def optimize_model(self):
        """یک بچ از تجربیات را از بافر گرفته و شبکه را یک مرحله آموزش می‌دهد"""
        if len(self.memory) < self.BATCH_SIZE:
            return None # تا زمانی که به اندازه کافی تجربه جمع نشده، آموزش نده
        
        experiences = self.memory.sample(self.BATCH_SIZE)
        batch = Experience(*zip(*experiences))

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)
        
        # برای next_stateها، آن‌هایی که پایانی (None) نیستند را جدا می‌کنیم
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), device=self.device, dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

        # Q(s_t, a)
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # V(s_{t+1})
        next_state_values = torch.zeros(self.BATCH_SIZE, device=self.device)
        next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()
        
        # محاسبه مقدار Q هدف (Expected Q values)
        expected_state_action_values = (next_state_values * self.GAMMA) + reward_batch

        # محاسبه خطا (Smooth L1 Loss)
        loss = F.mse_loss(state_action_values, expected_state_action_values.unsqueeze(1))
        
        # بهینه‌سازی
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100) # جلوگیری از انفجار گرادیان
        self.optimizer.step()
        
        return loss.item()

    # ==============================================================================
    # ۳. حلقه اصلی آموزش
    # ==============================================================================

    def train(self):
        self.episode_scores = []
        self.episode_losses = []
        print("شروع آموزش DQN برای زمان‌بندی تسک‌ها...")
        for i_episode in tqdm(range(self.NUM_EPISODES)):
            self.env.reset() # ریست کردن وضعیت منابع در ابتدای هر اپیزود
            total_reward = 0
            total_loss = 0
            num_optim_steps = 0
            
            # حلقه روی تمام تسک‌های ورودی
            for task_index in range(len(self.env.tasks)):
                # ۱. گرفتن وضعیت فعلی از محیط شما
                current_raw_state = self.env.temporary_state(task_index)
                # print(current_raw_state)
                normalized_state = current_raw_state
                state = torch.from_numpy(normalized_state.astype(np.float32)).unsqueeze(0).to(self.device)


                # ۲. انتخاب یک اقدام (منبع پردازشی)
                action = self.select_action(state)

                # ۳. اجرای اقدام در محیط و گرفتن نتایج
                _, next_raw_state, reward, done = self.env.step(task_index, action.item())
                
                # نرمال‌سازی وضعیت بعدی
                normalized_next_state =next_raw_state
                
                total_reward += reward
                reward_tensor = torch.tensor([reward], device=self.device)
                
                if done:
                    next_state = None
                else:
                    next_state = torch.from_numpy(normalized_next_state.astype(np.float32)).unsqueeze(0).to(self.device)


                # ۴. ذخیره تجربه در بافر
                self.memory.push(state, action, reward_tensor, next_state, done)
                
                # ۵. بهینه‌سازی مدل
                loss = self.optimize_model()
                if loss is not None:
                    total_loss += loss
                    num_optim_steps += 1
                    
                if done:
                    break
                    
            # ذخیره نتایج اپیزود
            self.episode_scores.append(total_reward)
            avg_loss = total_loss / num_optim_steps if num_optim_steps > 0 else 0
            self.episode_losses.append(avg_loss)
            
            # print(f"Episode {i_episode+1}/{NUM_EPISODES} | Score: {total_reward:.2f} | Avg Loss: {avg_loss:.4f}")

            # به‌روزرسانی شبکه هدف به صورت دوره‌ای
            if i_episode % self.TARGET_UPDATE == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())

        print("\nآموزش به پایان رسید!")

# ==============================================================================
# ۴. نمایش نتایج و تست نهایی
# ==============================================================================
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(self.episode_scores)
        plt.title('Reward per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(self.episode_losses)
        plt.title('Average Loss per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Loss')
        plt.grid(True)

        plt.tight_layout()
        plt.show()
        CURRENT_PATH=Path(__file__).resolve().parent
        MODEL_PATH = CURRENT_PATH/'dqn_scheduler_model.pth'
        torch.save(self.policy_net.state_dict(), MODEL_PATH)
