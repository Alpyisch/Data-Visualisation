import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

data = {
    'YIL': [2020, 2021, 2022, 2023, 2024],
    'BAŞVURAN SAYISI': [2436958, 2607903, 3243425, 3527443, 3120870],
    'SINAVA GİREN SAYISI': [2296138, 2416974, 3008287, 2995638, 2819362]
}

df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))

fig = plt.gcf()
fig.patch.set_facecolor('#FFF5E6')
ax = plt.gca()
ax.set_facecolor('#FFF5E6')

width = 0.35
x = df['YIL']
bar1 = plt.bar(x - width/2, df['BAŞVURAN SAYISI'], width, label='Başvuran Sayısı', color='#f1e6b8')
bar2 = plt.bar(x + width/2, df['SINAVA GİREN SAYISI'], width, label='Sınava Giren Sayısı', color='#f46e16')

plt.title('Yıllara Göre YKS Başvuran ve Sınava Giren Öğrenci Sayıları', fontsize=14, pad=20)
plt.xlabel('Yıl', fontsize=12)
plt.ylabel('Öğrenci Sayısı (Milyon)', fontsize=12)
plt.xticks(x)

def millions_formatter(x, pos):
    return f'{x/1e6:.1f}M'
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))

plt.grid(False)

for bar in [bar1, bar2]:
    for rect in bar:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., height,
                f'{height/1e6:.1f}M',
                ha='center', va='bottom', fontsize=8)

plt.legend()
plt.tight_layout()
plt.show()
