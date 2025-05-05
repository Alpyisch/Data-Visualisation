import pandas as pd
import matplotlib.pyplot as plt

data = {
    'KIZ': [114, 63, 109, 50, 131, 39, 147, 130, 122, 151, 139, 46, 147, 14, 150, 
            124, 187, 131, 20, 25, 62, 76, 71, 31, 125, 44, 77, 133, 54, 89, 69, 
            102, 135, 144, 177, 126, 133, 67, 66],
    'ERKEK': [179, 57, 221, 65, 186, 49, 212, 211, 135, 263, 228, 102, 261, 23, 303, 
              181, 452, 183, 26, 44, 103, 86, 113, 46, 189, 69, 180, 222, 66, 151, 
              105, 227, 207, 236, 273, 152, 275, 80, 126]
}

df = pd.DataFrame(data)

toplam_kiz = df['KIZ'].sum()
toplam_erkek = df['ERKEK'].sum()

plt.figure(figsize=(8, 8), facecolor='#f6f6e9')
ax = plt.subplot(111)
ax.set_facecolor('#f6f6e9')

plt.title('Toplam Kız ve Erkek Öğrenci Oranları', fontsize=16, pad=20)

labels = ['Kız', 'Erkek']
sizes = [toplam_kiz, toplam_erkek]
colors = ['#f46e1b', '#f1e6b8']
explode = (0.05, 0)

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140,
        textprops={'fontsize': 14})

plt.axis('equal')

plt.tight_layout()
plt.show()
