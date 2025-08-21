import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import arabic_reshaper
from bidi.algorithm import get_display

# مسیر فایل فونت که دانلود کرده‌ای
font_path = r"C:\Users\Aragorn\Desktop\Projects\fogZoneSim\Resource\utilize\Algorithms\DRL\Scheduling\Vazirmatn-Light.ttf"
prop = fm.FontProperties(fname=font_path)

def fa_text(txt):
    return get_display(arabic_reshaper.reshape(txt))

x = np.linspace(0, 10, 100)
y1 = np.sin(x) + np.random.normal(0, 0.1, 100)
y2 = np.cos(x) + np.random.normal(0, 0.1, 100)

plt.figure(figsize=(10,6))

plt.plot(x, y1, label=fa_text("سیگنال ۱ (سینوس)"), color="#1f77b4")
plt.plot(x, y2, label=fa_text("سیگنال ۲ (کسینوس)"), color="#ff7f0e")

plt.grid(True, linestyle="--", alpha=0.6)

plt.title(fa_text("نمونه نمودار خطی با طراحی زیبا"),fontproperties=prop, fontsize=12)
plt.xlabel(fa_text("محور زمان"), fontproperties=prop, fontsize=12)
plt.ylabel(fa_text("دامنه"), fontproperties=prop, fontsize=12)

plt.legend(prop=prop)

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

plt.show()