from Env.engine import Engine
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

# ==============================================================================
# ۱. هایپرپارامترها و تنظیمات اولیه
# ==============================================================================

# فرض می‌کنیم شما کلاس خود را در فایلی به نام a_star_env import کرده‌اید
# from your_env_file import YourEnvClass  # <--- نام فایل و کلاس خود را اینجا قرار دهید

# یک نمونه از محیط خود بسازید
# env = YourEnvClass() # <--- نمونه‌سازی کلاس شما

# *** برای اجرای این کد به تنهایی، از کلاس شبیه‌ساز زیر استفاده می‌کنیم ***
# *** شما باید این بخش را کامنت کرده و خطوط بالا را فعال کنید ***
class MockEnv:
    def __init__(self, num_resources=5, num_tasks=50):
        self.num_resources = num_resources
        self.num_tasks = num_tasks
        self.resources = np.zeros(num_resources)
    def reset(self): self.resources = np.zeros(self.num_resources); return self.resources
    def temporary_state(self, task_index): return self.resources
    def normalize_state(self, state): return state / (np.sum(state) + 1e-8)
    def step(self, task_index, action):
        old_state = self.resources.copy()
        self.resources[action] += np.random.uniform(0.5, 1.5) # افزودن بار تسک
        reward = -self.resources[action] # پاداش منفی برای تشویق به انتخاب منابع با بار کمتر
        done = (task_index == self.num_tasks - 1)
        return old_state, self.resources.copy(), reward, done
env = Engine()
# *** پایان بخش شبیه‌ساز ***


# هایپرپارامترهای DQN
BATCH_SIZE = 128            # بزرگ‌تر از حالت قبلی برای نمونه‌گیری پایدارتر
GAMMA = 0.95                # تنزیل ملایم برای توجه به آینده ولی با تمرکز بر حال
EPS_START = 1.0             # اکتشاف کامل در ابتدا (100٪ اکشن تصادفی)
EPS_END = 0.05              # در پایان 5٪ رفتار تصادفی حفظ میشه
EPS_DECAY = 5000            # آهسته‌تر شدن روند کاهش اکتشاف برای کاهش bias
TARGET_UPDATE = 500         # به‌روزرسانی مکررتر شبکه هدف برای سازگاری بهتر
LR = 1e-6                   # نرخ یادگیری معقول برای شبکه کوچک تا متوسط
NUM_EPISODES = 1000         # اپیزودهای بیشتر برای پوشش بیشتر وضعیت‌ها
NUM_TASKS = 200              # بسته به اندازه مسئله‌ات خوبه
STATE_SIZE = 5              # فرض بر اینکه 5 ویژگی مهم در state داری
ACTION_SIZE = 5


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ساختن شبکه‌ها، بهینه‌ساز و بافر
policy_net = QNetwork(STATE_SIZE, ACTION_SIZE).to(device)
target_net = QNetwork(STATE_SIZE, ACTION_SIZE).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LR)
memory = ReplayBuffer(1000000)

steps_done = 0

# ==============================================================================
# ۲. توابع کمکی برای انتخاب اقدام و بهینه‌سازی
# ==============================================================================

def select_action(state):
    """انتخاب اقدام بر اساس سیاست اپسیلون-حریصانه"""
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # از شبکه اصلی برای انتخاب بهترین اقدام استفاده کن
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        # یک اقدام تصادفی انتخاب کن
        return torch.tensor([[random.randrange(ACTION_SIZE)]], device=device, dtype=torch.long)

def optimize_model():
    """یک بچ از تجربیات را از بافر گرفته و شبکه را یک مرحله آموزش می‌دهد"""
    if len(memory) < BATCH_SIZE:
        return None # تا زمانی که به اندازه کافی تجربه جمع نشده، آموزش نده
    
    experiences = memory.sample(BATCH_SIZE)
    batch = Experience(*zip(*experiences))

    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    
    # برای next_stateها، آن‌هایی که پایانی (None) نیستند را جدا می‌کنیم
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

    # Q(s_t, a)
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # V(s_{t+1})
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    
    # محاسبه مقدار Q هدف (Expected Q values)
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # محاسبه خطا (Smooth L1 Loss)
    loss = F.mse_loss(state_action_values, expected_state_action_values.unsqueeze(1))
    
    # بهینه‌سازی
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100) # جلوگیری از انفجار گرادیان
    optimizer.step()
    
    return loss.item()

# ==============================================================================
# ۳. حلقه اصلی آموزش
# ==============================================================================

episode_scores = []
episode_losses = []

print("شروع آموزش DQN برای زمان‌بندی تسک‌ها...")
for i_episode in tqdm(range(NUM_EPISODES)):
    env.reset() # ریست کردن وضعیت منابع در ابتدای هر اپیزود
    total_reward = 0
    total_loss = 0
    num_optim_steps = 0
    
    # حلقه روی تمام تسک‌های ورودی
    for task_index in range(env.tasks.number_of_task):
        # ۱. گرفتن وضعیت فعلی از محیط شما
        current_raw_state = env.temporary_state(task_index)
        # print(current_raw_state)
        normalized_state = current_raw_state
        state = torch.from_numpy(normalized_state.astype(np.float32)).unsqueeze(0).to(device)


        # ۲. انتخاب یک اقدام (منبع پردازشی)
        action = select_action(state)

        # ۳. اجرای اقدام در محیط و گرفتن نتایج
        _, next_raw_state, reward, done = env.step(task_index, action.item())
        
        # نرمال‌سازی وضعیت بعدی
        normalized_next_state =next_raw_state
        
        total_reward += reward
        reward_tensor = torch.tensor([reward], device=device)
        
        if done:
            next_state = None
        else:
            next_state = torch.from_numpy(normalized_next_state.astype(np.float32)).unsqueeze(0).to(device)


        # ۴. ذخیره تجربه در بافر
        memory.push(state, action, reward_tensor, next_state, done)
        
        # ۵. بهینه‌سازی مدل
        loss = optimize_model()
        if loss is not None:
            total_loss += loss
            num_optim_steps += 1
            
        if done:
            break
            
    # ذخیره نتایج اپیزود
    episode_scores.append(total_reward)
    avg_loss = total_loss / num_optim_steps if num_optim_steps > 0 else 0
    episode_losses.append(avg_loss)
    
    # print(f"Episode {i_episode+1}/{NUM_EPISODES} | Score: {total_reward:.2f} | Avg Loss: {avg_loss:.4f}")

    # به‌روزرسانی شبکه هدف به صورت دوره‌ای
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

print("\nآموزش به پایان رسید!")

# ==============================================================================
# ۴. نمایش نتایج و تست نهایی
# ==============================================================================

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(episode_scores)
plt.title('Reward per Episode')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(episode_losses)
plt.title('Average Loss per Episode')
plt.xlabel('Episode')
plt.ylabel('Loss')
plt.grid(True)

plt.tight_layout()
plt.show()

# تست مدل نهایی
print("\nشروع تست مدل آموزش‌دیده...")
env.reset()
test_total_reward = 0
for task_index in range(NUM_TASKS):
    raw_state = env.temporary_state(task_index)
    norm_state = raw_state
    state_tensor = torch.tensor([norm_state], device=device, dtype=torch.float32)
    with torch.no_grad():
        # انتخاب بهترین اقدام بر اساس سیاست یادگرفته‌شده
        action = policy_net(state_tensor).max(1)[1].view(1, 1)
    
    _, _, reward, done = env.step(task_index, action.item())
    test_total_reward += reward
    if done:
        break

print(f"امتیاز نهایی در فاز تست: {test_total_reward:.2f}")

# ذخیره مدل نهایی (اختیاری)
torch.save(policy_net.state_dict(), 'dqn_scheduler_model_modified5.pth')

# rtx=Engine()


# print(rtx.max_S_element_val_for_norm)

# for i in range(rtx.tasks.number_of_task):
#     action=random.randint(0, 4)
#     print(f"number of task: {i}")
#     print(f"state before action is {rtx.get_current_status()}")
#     print(f"state with normalize is {rtx.normalize_state(rtx.state)}")
#     rtx.step(i,action)
#     print(f"state after action is {rtx.get_current_status()}")
#     print("**************************************************")
    
# # rtx.temporary_state(3)
# # rtx.step(3,2)

# # print(rtx.step(19,3))
# # print(f"\n\n state is: \n\n {rtx.state}  \n\n\n temp_state is: \n\n f{rtx.temp_state}")

# rtx.reset()

# print(f"\n\n after reset state is: \n\n {rtx.state}  \n\n\n temp_state is: \n\n f{rtx.temp_state}")



import torch
import torch.nn as nn
import numpy as np

# ==============================================================================
# ۱. تعریف مجدد ساختار شبکه و محیط
# ==============================================================================

# تعریف مجدد کلاس شبکه عصبی (باید دقیقا مشابه زمان آموزش باشد)
# پارامترهای مدل
STATE_SIZE = 5
ACTION_SIZE = 5
MODEL_PATH = 'dqn_scheduler_model_modified5.pth' # مسیر فایل ذخیره شده

# ساخت یک نمونه از شبکه
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = QNetwork(STATE_SIZE, ACTION_SIZE).to(device)

# بارگذاری وزن‌های آموزش‌دیده
try:
    model.load_state_dict(torch.load(MODEL_PATH))
    print(f"مدل با موفقیت از مسیر '{MODEL_PATH}' بارگذاری شد.")
except FileNotFoundError:
    print(f"خطا: فایل مدل در مسیر '{MODEL_PATH}' پیدا نشد. لطفاً ابتدا مدل را آموزش و ذخیره کنید.")
    exit()


# قرار دادن مدل در حالت ارزیابی (بسیار مهم)
# این کار لایه‌هایی مثل Dropout یا BatchNorm را غیرفعال می‌کند
model.eval()

# ==============================================================================
# ۳. اجرای مدل روی تسک‌های جدید و نمایش خروجی
# ==============================================================================

def schedule_tasks_with_model(trained_model, env_instance, num_tasks):
    """
    از مدل آموزش‌دیده برای تخصیص مجموعه‌ای از تسک‌ها استفاده می‌کند.
    
    Args:
        trained_model: مدل QNetwork که وزن‌های آن بارگذاری شده.
        env_instance: یک نمونه از کلاس محیط شما.
        num_tasks: تعداد تسک‌هایی که باید زمان‌بندی شوند.
        
    Returns:
        یک آرایه NumPy شامل دنباله‌ای از اقدامات (شماره منابع) انتخاب‌شده.
    """
    print(f"\nشروع زمان‌بندی برای {num_tasks} تسک جدید...")
    
    # ریست کردن محیط
    env_instance=Engine()
    env_instance.reset()
    action_sequence = []
    
    # این حلقه باید با torch.no_grad() اجرا شود تا محاسبات گرادیان انجام نشود
    with torch.no_grad():
        for task_index in range(num_tasks):
            # گرفتن وضعیت فعلی از محیط
            raw_state = env_instance.temporary_state(task_index)
            normalized_state =raw_state
            state_tensor = torch.tensor([normalized_state], device=device, dtype=torch.float32)

            # استفاده از مدل برای پیش‌بینی بهترین اقدام (بدون اپسیلون)
            # .max(1)[1] مقدار بیشینه و اندیس آن را برمی‌گرداند. ما به اندیس نیاز داریم.
            action = trained_model(state_tensor).max(1)[1].item()
            
            # ذخیره اقدام انتخاب‌شده
            action_sequence.append(action)
            
            # به‌روزرسانی محیط با اقدام انجام‌شده
            _, _, _, done = env_instance.step(task_index, action)
            
            if done:
                print("همه تسک‌ها زمان‌بندی شدند.")
                break
                
    return np.array(action_sequence)

# --- اجرای نمونه ---
# یک نمونه از محیط خود بسازید
test_env =Engine()
# تعداد تسک‌های مورد نظر برای تست را مشخص کنید
NUM_TEST_TASKS = 100

# اجرای تابع زمان‌بندی
final_schedule = schedule_tasks_with_model(model, test_env, NUM_TEST_TASKS)

# نمایش آرایه نهایی انتخاب‌ها
print("\n" + "="*40)
print("final result")
# print(f"دنباله تخصیص تسک‌ها به منابع (منبع 0 تا {ACTION_SIZE-1}):")
print(f"{final_schedule}")
print("="*40)

# # # مثال: تسک شماره ۰ به منبع `final_schedule[0]`، تسک ۱ به `final_schedule[1]` و ... تخصیص یافت.


# import torch
# import torch.nn as nn
# import torch.optim as optim
# import torch.nn.functional as F
# import numpy as np
# import random
# from collections import deque, namedtuple
# import matplotlib.pyplot as plt
# import os
# from tqdm import tqdm

# # ==============================================================================
# # ۱. هایپرپارامترها و تنظیمات اولیه
# # ==============================================================================
# BUFFER_SIZE = int(1e5)
# BATCH_SIZE = 64
# GAMMA = 0.99
# TAU = 1e-3
# LR = 1e-4
# UPDATE_EVERY = 4
# TARGET_UPDATE_EVERY = 100
# MAX_GRAD_NORM = 1.0

# # تعریف دستگاه (CPU یا GPU)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # ==============================================================================
# # ۲. قالب محیط سفارشی (این بخش را با منطق خود کامل کنید)
# # ==============================================================================
# class MyCustomEnv:
#     """
#     این کلاس، محیط سفارشی شما برای مسئله زمان‌بندی تسک است.
#     شما باید منطق اصلی خود را در متدهای این کلاس پیاده‌سازی کنید.
#     """
#     def __init__(self, num_actions=5, state_vector_size=5):
#         """
#         سازنده محیط شما.
#         """
#         self.action_size = num_actions
#         self.state_size = state_vector_size
        
#         # *** بسیار مهم ***
#         # یک مقدار منطقی برای ماکسیمم مقدار یک عنصر در وکتور وضعیت خام تعریف کنید.
#         # این مقدار برای نرمال‌سازی وضعیت استفاده خواهد شد.
#         self.max_state_value = 1000.0  # <--- این مقدار را با توجه به محیط خودتان تنظیم کنید

#         print("محیط سفارشی شما با موفقیت ساخته شد!")

#     def reset(self):
#         """
#         محیط را برای یک اپیزود جدید آماده می‌کند و وضعیت اولیه خام را برمی‌گرداند.
#         """
#         # TODO: منطق ریست کردن محیط خود را در اینجا بنویسید.
#         # برای مثال: صفر کردن بار منابع، آماده کردن اولین تسک و ...
        
#         # مثال: بازگرداندن یک وکتور وضعیت صفر به عنوان وضعیت اولیه
#         initial_state_raw = np.zeros(self.state_size, dtype=np.float32)
#         return initial_state_raw

#     def step(self, action):
#         """
#         یک اقدام را اجرا کرده و نتیجه را به صورت (next_state_raw, reward, done, info) برمی‌گرداند.
#         """
#         # TODO: منطق اصلی گام برداشتن در محیط را اینجا بنویسید.
#         # ۱. بر اساس 'action' دریافتی، وضعیت داخلی محیط را تغییر دهید (مثلاً تخصیص تسک).
#         # ۲. پاداش (reward) را بر اساس کیفیت اقدام محاسبه کنید.
#         # ۳. بررسی کنید که آیا اپیزود تمام شده است یا نه (done).
#         # ۴. وضعیت جدید خام (next_state_raw) را برای تصمیم بعدی عامل ایجاد کنید.
        
#         # مثال فرضی:
#         next_state_raw = np.random.rand(self.state_size).astype(np.float32)
#         reward = np.random.uniform(-1, 1) 
#         done = False 
#         info = {} 
        
#         return next_state_raw, reward, done, info

#     def get_state_size(self):
#         return self.state_size

#     def get_action_size(self):
#         return self.action_size

# # ==============================================================================
# # ۳. توابع و کلاس‌های کمکی (بدون تغییر)
# # ==============================================================================

# def normalize_state(state_raw, max_state_element_value):
#     """وضعیت خام را به یک محدوده مناسب برای شبکه عصبی نرمال می‌کند."""
#     norm_s = np.copy(state_raw).astype(np.float32)
#     if max_state_element_value > 0:
#         norm_s /= max_state_element_value
#     norm_s = np.clip(norm_s, 0.0, 2.0)
#     return norm_s

# class QNetwork(nn.Module):
#     def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64):
#         super(QNetwork, self).__init__()
#         self.seed = torch.manual_seed(seed)
#         self.fc1 = nn.Linear(state_size, fc1_units)
#         self.fc2 = nn.Linear(fc1_units, fc2_units)
#         self.fc3 = nn.Linear(fc2_units, action_size)
#     def forward(self, state):
#         x = F.relu(self.fc1(state))
#         x = F.relu(self.fc2(x))
#         return self.fc3(x)

# Experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])

# class ReplayBuffer:
#     def __init__(self, action_size, buffer_size, batch_size, seed):
#         self.memory = deque(maxlen=buffer_size)
#         self.batch_size = batch_size
#         self.seed = random.seed(seed)
#         np.random.seed(seed)
#     def add(self, state, action, reward, next_state, done):
#         e = Experience(state, action, reward, next_state, done)
#         self.memory.append(e)
#     def sample(self):
#         experiences = random.sample(self.memory, k=self.batch_size)
#         states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
#         actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
#         rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
#         next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
#         dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
#         return (states, actions, rewards, next_states, dones)
#     def __len__(self):
#         return len(self.memory)

# class DQNAgent:
#     def __init__(self, state_size, action_size, seed):
#         self.state_size = state_size
#         self.action_size = action_size
#         self.seed = random.seed(seed)
#         np.random.seed(seed)
#         self.qnetwork_local = QNetwork(state_size, action_size, seed).to(device)
#         self.qnetwork_target = QNetwork(state_size, action_size, seed).to(device)
#         self.optimizer = optim.Adam(self.qnetwork_local.parameters(), lr=LR)
#         self.memory = ReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE, seed)
#         self.t_step = 0
#         self.target_update_counter = 0

#     def step(self, state_norm, action, reward, next_state_norm, done):
#         self.memory.add(state_norm, action, reward, next_state_norm, done)
#         current_loss = None 
#         self.t_step = (self.t_step + 1) % UPDATE_EVERY
#         if self.t_step == 0:
#             if len(self.memory) > BATCH_SIZE:
#                 experiences = self.memory.sample()
#                 current_loss = self.learn(experiences, GAMMA)
#         self.target_update_counter = (self.target_update_counter + 1) % TARGET_UPDATE_EVERY
#         if self.target_update_counter == 0:
#             self.soft_update(self.qnetwork_local, self.qnetwork_target, TAU)
#         return current_loss

#     def act(self, state_norm, eps=0.):
#         state_t = torch.from_numpy(state_norm).float().unsqueeze(0).to(device)
#         self.qnetwork_local.eval()
#         with torch.no_grad():
#             action_values = self.qnetwork_local(state_t)
#         self.qnetwork_local.train()
#         if random.random() > eps:
#             return np.argmax(action_values.cpu().data.numpy())
#         else:
#             return random.choice(np.arange(self.action_size))

#     def learn(self, experiences, gamma):
#         states, actions, rewards, next_states, dones = experiences
#         Q_targets_next = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)
#         Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))
#         Q_expected = self.qnetwork_local(states).gather(1, actions)
#         loss = F.mse_loss(Q_expected, Q_targets)
#         self.optimizer.zero_grad()
#         loss.backward()
#         torch.nn.utils.clip_grad_norm_(self.qnetwork_local.parameters(), MAX_GRAD_NORM)
#         self.optimizer.step()
#         return loss.item()

#     def soft_update(self, local_model, target_model, tau):
#         for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
#             target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)

#     def save_model(self, filepath="dqn_model.pth"):
#         torch.save(self.qnetwork_local.state_dict(), filepath)
#         print(f"\nModel saved to {filepath}")

#     def load_model(self, filepath="dqn_model.pth"):
#         if os.path.exists(filepath):
#             state_dict = torch.load(filepath, map_location=device)
#             self.qnetwork_local.load_state_dict(state_dict)
#             self.qnetwork_target.load_state_dict(state_dict)
#             self.qnetwork_local.eval() 
#             self.qnetwork_target.eval()
#             print(f"Model loaded from {filepath} and set to evaluation mode.")
#         else:
#             print(f"Error: No model found at {filepath}.")
#             raise FileNotFoundError(f"Model file not found: {filepath}")

# # ==============================================================================
# # ۴. تابع آموزش (با تغییر جزئی برای هماهنگی با محیط جدید)
# # ==============================================================================

# def train_dqn(env, agent, n_episodes=2000, max_t_per_episode=100, eps_start=1.0, eps_end=0.01, eps_decay=0.995, model_save_path="dqn_custom_env_model.pth"):
#     all_scores = []
#     scores_window = deque(maxlen=100)
#     all_episode_avg_losses = []
#     eps = eps_start

#     # *** تغییر کلیدی: گرفتن مقدار نرمال‌سازی از نمونه محیط جدید ***
#     max_s_val_for_norm = env.max_S_element_val_for_norm

#     print(f"Starting training for {n_episodes} episodes...")
#     print(f"State normalization constant: {max_s_val_for_norm:.2f}")

#     for i_episode in tqdm(range(1, n_episodes + 1)):
#         state_raw = env.reset()
#         state_norm = normalize_state(state_raw, max_s_val_for_norm)
        
#         episode_score = 0
#         current_episode_losses = []

#         for t in range(max_t_per_episode):
#             action = agent.act(state_norm, eps)
            
#             next_state_raw, reward, done, _ = env.step(action)
#             next_state_norm = normalize_state(next_state_raw, max_s_val_for_norm)
            
#             loss_value = agent.step(state_norm, action, reward, next_state_norm, done) 
            
#             state_norm = next_state_norm
#             episode_score += reward
#             if loss_value is not None:
#                 current_episode_losses.append(loss_value)
#             if done:
#                 break
        
#         scores_window.append(episode_score)
#         all_scores.append(episode_score)
#         eps = max(eps_end, eps_decay * eps)
        
#         avg_loss_str = "N/A"
#         if current_episode_losses:
#             avg_loss_this_episode = np.mean(current_episode_losses)
#             all_episode_avg_losses.append(avg_loss_this_episode)
#             avg_loss_str = f"{avg_loss_this_episode:.4f}"
#         else:
#             all_episode_avg_losses.append(np.nan)
#         # این بخش از کد برای جلوگیری از پر شدن ترمینال، تنها هر ۱۰۰ اپیزود یکبار چاپ می‌کند
#         # if i_episode % 100 == 0:
#         #    print(f'\rEpisode {i_episode}/{n_episodes}\tAvg Score: {np.mean(scores_window):.3f}\tAvg Loss: {avg_loss_str}\tEpsilon: {eps:.3f}')
            
#     agent.save_model(model_save_path)
#     return all_scores, all_episode_avg_losses

# # ==============================================================================
# # ۵. اجرای اصلی برنامه (آموزش، رسم نمودار و تست)
# # ==============================================================================

# if __name__ == '__main__':
#     ENV_SEED = 42
#     AGENT_SEED = 42 
#     NUM_EPISODES_TRAIN = 1000 # برای اجرای سریع‌تر، تعداد اپیزودها را کم می‌کنیم
#     TASKS_PER_EPISODE = 100
#     MODEL_SAVE_FILENAME = "my_custom_scheduler_model.pth"

#     # تنظیم seed برای تکرارپذیری نتایج
#     random.seed(ENV_SEED)
#     np.random.seed(ENV_SEED)
#     torch.manual_seed(AGENT_SEED)
#     if device.type == "cuda":
#         torch.cuda.manual_seed_all(AGENT_SEED)

#     print(f"Using device: {device}")

#     # *** تغییر کلیدی: ساختن نمونه از محیط سفارشی شما ***
#     env = Engine()
    
#     state_size = 5
#     action_size = 5
    
#     print(f"State size: {state_size}, Action size: {action_size}")
#     agent = DQNAgent(state_size=state_size, action_size=action_size, seed=AGENT_SEED)

#     # --- شروع آموزش ---
#     scores, losses = train_dqn(
#         env, 
#         agent, 
#         n_episodes=NUM_EPISODES_TRAIN, 
#         max_t_per_episode=TASKS_PER_EPISODE,
#         model_save_path=MODEL_SAVE_FILENAME
#     )
#     print("\n--- Training Finished ---")

#     # --- رسم نمودارها ---
#     fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
#     axs[0].plot(np.arange(1, len(scores) + 1), scores, label='Score per Episode')
#     axs[0].set_title('Training Performance: Scores')
#     axs[0].set_ylabel('Total Reward')
#     axs[0].grid(True)
#     axs[0].legend()
    
#     valid_losses = [l for l in losses if not np.isnan(l)]
#     valid_indices = [i+1 for i, l in enumerate(losses) if not np.isnan(l)]
#     axs[1].plot(valid_indices, valid_losses, label='Average Loss', color='green')
#     axs[1].set_title('Training Performance: Loss')
#     axs[1].set_xlabel('Episode #')
#     axs[1].set_ylabel('Average Loss')
#     axs[1].grid(True)
#     axs[1].legend()
#     plt.tight_layout()
#     plt.show()

#     # --- تست مدل آموزش‌دیده ---
#     print("\n--- Testing the Trained Agent ---")
#     try:
#         test_agent = DQNAgent(state_size=state_size, action_size=action_size, seed=AGENT_SEED + 1) 
#         test_agent.load_model(MODEL_SAVE_FILENAME)
        
#         test_env = MyCustomEnv(num_actions=5, state_vector_size=5) # استفاده از محیط سفارشی برای تست
        
#         max_s_val_for_norm_test = test_env.max_state_value # *** تغییر کلیدی ***

#         state_raw = test_env.reset()
#         total_test_reward = 0
#         num_test_tasks = 20
#         action_sequence = []

#         print(f"\nRunning loaded model for {num_test_tasks} tasks...")
#         for i_task in range(num_test_tasks):
#             state_norm = normalize_state(state_raw, max_s_val_for_norm_test)
#             action = test_agent.act(state_norm, eps=0.0) # eps=0.0 برای انتخاب بهترین اقدام
#             action_sequence.append(action)
            
#             next_state_raw, reward, done, _ = test_env.step(action)
            
#             state_raw = next_state_raw
#             total_test_reward += reward
#             if done:
#                 break

#         print(f"\nTotal reward over {num_test_tasks} test tasks: {total_test_reward:.3f}")
#         print(f"Sequence of actions taken: {np.array(action_sequence)}")

#     except FileNotFoundError:
#         print(f"TESTING SKIPPED: Model file '{MODEL_SAVE_FILENAME}' not found.")
#     except Exception as e:
#         print(f"An error occurred during testing: {e}")






# from Env import Engine
# import random
# env=Engine()

# random.seed(42)


# for epoch in range(1):
#     print(f"**************************** epoch {epoch}****************************************")
#     for i in range(env.tasks.number_of_task):
#         action=random.randint(0,4)
#         current_status=env.get_current_status()
#         current_status_normal=env.normalize_state(current_status)
#         current_utilize_status=env.temporary_state(i)
#         current_utilize_status_norm=env.normalize_state(current_utilize_status)
#         print(f"------------------------------in epoch{epoch} and task{i}-------------------------------------------")
#         print(f"current_state is{current_status}  \n current norm state is {current_status_normal}")
        
#         print(f"resource is {env.resources.get_current_status()}")
#         print(f"temporary current_state is{current_utilize_status}  \n temporary current norm state is {current_utilize_status_norm}")
#         print(f"action is {action}")
#         old_state,new_state_ret,reward,done=env.step(i,action)
#         new_status=env.get_current_status()
#         print(f"reward is {reward} and done is {done}")
#         print(f" resource after action {env.resources.get_current_status()}")
#         print(f"return new state is {new_state_ret}   \n new state is {new_status}")
    