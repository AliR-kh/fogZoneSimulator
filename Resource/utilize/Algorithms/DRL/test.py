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

# پارامترهای مدل
STATE_SIZE = 5
ACTION_SIZE = 5
MODEL_PATH = 'dqn_scheduler_model_modified4.pth' # مسیر فایل ذخیره شده

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
    
    
    env_instance=Engine()
    
    # ریست کردن محیط
    env_instance.reset()
    action_sequence = []
    
    # این حلقه باید با torch.no_grad() اجرا شود تا محاسبات گرادیان انجام نشود
    with torch.no_grad():
        for task_index in range(num_tasks):
            # گرفتن وضعیت فعلی از محیط
            raw_state = env_instance.temporary_state(task_index)
            normalized_state = raw_state
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
NUM_TEST_TASKS = 200

# اجرای تابع زمان‌بندی
final_schedule = schedule_tasks_with_model(model, test_env, NUM_TEST_TASKS)

# نمایش آرایه نهایی انتخاب‌ها
print("\n" + "="*40)
print("final result")
# print(f"دنباله تخصیص تسک‌ها به منابع (منبع 0 تا {ACTION_SIZE-1}):")
print(f"{final_schedule}")
print("="*40)


import numpy as np
import matplotlib.pyplot as plt

# داده‌های شما:
data = np.array([
    0, 2, 0, 3, 3, 1, 0, 3, 2, 4, 4, 2, 1, 0, 3, 0, 3, 2, 4, 1, 1, 0, 1, 3, 1, 3, 1, 2, 1, 1, 2, 4, 1, 1, 0, 3, 2,
    1, 2, 0, 3, 4, 4, 2, 3, 0, 3, 1, 4, 2, 3, 3, 0, 1, 4, 2, 1, 4, 3, 1, 4, 0, 2, 1, 3, 0, 0, 2, 3, 1, 4, 3, 0, 3,
    4, 2, 3, 3, 4, 2, 1, 1, 0, 4, 3, 3, 2, 3, 1, 1, 0, 3, 2, 4, 2, 1, 0, 3, 0, 3, 2, 1, 4, 2, 0, 1, 4, 3, 2, 1, 4,
    3, 0, 2, 1, 3, 3, 3, 0, 1, 3, 2, 4, 1, 0, 3, 4, 2, 3, 0, 4, 1, 2, 1, 0, 1, 4, 3, 2, 1, 0, 3, 0, 2, 1, 3, 4, 0,
    0, 2, 1, 1, 4, 0, 3, 4, 3, 1, 2, 1, 0, 2, 1, 0, 3, 4, 3, 3, 3, 0, 2, 1, 3, 4, 0, 3, 2, 3, 0, 4, 2, 1, 0, 3, 2,
    4, 3, 1, 0, 0, 3, 2, 4, 1, 4, 2, 0, 1, 4, 0
])

# محاسبه تعداد هر عدد
unique, counts = np.unique(final_schedule, return_counts=True)

# چاپ مقادیر
for u, c in zip(unique, counts):
    print(f"عدد {u} تکرار شده است: {c} بار")

# رسم نمودار
plt.bar(unique, counts, color='skyblue')
plt.xlabel('عدد')
plt.ylabel('تعداد تکرار')
plt.title('تعداد تکرار هر عدد')
plt.xticks(unique)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()