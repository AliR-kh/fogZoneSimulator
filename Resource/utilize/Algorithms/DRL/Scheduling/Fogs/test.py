from utilize.Algorithms.DRL.Scheduling.Fogs.env import Engine
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from pathlib import Path

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




class RunTest():
    def __init__(self,tasks,resources):
        self.tasks=tasks
        self.resources=resources
        self._init_model() 
        
    def _init_model(self):
        STATE_SIZE = 5
        ACTION_SIZE = 5
        CURRENT_PATH=Path(__file__).resolve().parent
        MODEL_PATH = CURRENT_PATH/'dqn_scheduler_model.pth' # مسیر فایل ذخیره شده
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = QNetwork(STATE_SIZE, ACTION_SIZE).to(self.device)
        try:
            self.model.load_state_dict(torch.load(MODEL_PATH))
            self.model.eval()
        # print(f"مدل با موفقیت از مسیر '{MODEL_PATH}' بارگذاری شد.")
        except FileNotFoundError:
        # print(f"خطا: فایل مدل در مسیر '{MODEL_PATH}' پیدا نشد. لطفاً ابتدا مدل را آموزش و ذخیره کنید.")
            exit()


# قرار دادن مدل در حالت ارزیابی (بسیار مهم)
# این کار لایه‌هایی مثل Dropout یا BatchNorm را غیرفعال می‌کند
    def schedule_tasks_with_model(self):
        env_instance=Engine(resources=self.resources,tasks=self.tasks)
        env_instance.reset()
        action_sequence = []
        
        # این حلقه باید با torch.no_grad() اجرا شود تا محاسبات گرادیان انجام نشود
        with torch.no_grad():
            for task_index in range(len(env_instance.tasks)):
                # گرفتن وضعیت فعلی از محیط
                env_instance.temporary_state(task_index)
                normalized_state =env_instance.temp_state
                state_tensor = torch.tensor(np.array([normalized_state]), device=self.device, dtype=torch.float32)

                # استفاده از مدل برای پیش‌بینی بهترین اقدام (بدون اپسیلون)
                # .max(1)[1] مقدار بیشینه و اندیس آن را برمی‌گرداند. ما به اندیس نیاز داریم.
                action = self.model(state_tensor).max(1)[1].item()
                
                # ذخیره اقدام انتخاب‌شده
                action_sequence.append(action)
                
                # به‌روزرسانی محیط با اقدام انجام‌شده
                _, _, _, done = env_instance.step(task_index, action)
                
                if done:
                    break
                    
        return action_sequence
