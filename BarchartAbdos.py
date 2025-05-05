import pandas as pd
import matplotlib.pyplot as plt

file_path = "ABDOS.xlsx"
df = pd.read_excel(file_path, sheet_name="Sayfa1")

df_grouped = df.groupby("Üniversite Adı").agg({
    "ABDÖS": "sum",
    "Kayıtlı Öğrenci Sayısı": "sum"
}).reset_index()

plt.figure(figsize=(15, 8), facecolor='#f6f6e9')
bar_width = 0.4
index = range(len(df_grouped))

plt.bar(index, df_grouped["ABDÖS"], bar_width, label='ABDÖS', color='#73361C')
plt.bar([i + bar_width for i in index], df_grouped["Kayıtlı Öğrenci Sayısı"], bar_width, label='Kayıtlı Öğrenci Sayısı', color='#f46e1b')

plt.xlabel('Üniversiteler')
plt.ylabel('Sayı')
plt.title('Üniversitelere Göre ABDOS ve Kayıtlı Öğrenci Sayısı')

plt.xticks([i + bar_width / 2 for i in index], df_grouped["Üniversite Adı"], rotation=90)

plt.grid(False)

plt.gca().set_facecolor('#f6f6e9')

plt.legend()
plt.tight_layout()
plt.show()
