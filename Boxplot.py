import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

file_path = r"C:\Users\alper\OneDrive\Masaüstü\Ders Notları\3.Sınıf\Veri Gorsellestirme\ybs_taban_puanlari.xlsx"
df = pd.read_excel(file_path)

for year in [2020, 2021, 2022, 2023, 2024]:
    if year in df.columns:
        df[year] = (
            df[year]
            .astype(str)
            .str.replace("\n", "", regex=False)
            .str.replace(" ", "", regex=False)
            .str.strip()
        )
        df[year] = df[year].replace(["nan", "——", "—", "-", "Dolmadı", "NA", "", "None"], np.nan)
        
        try:
            df[year] = pd.to_numeric(df[year], errors='coerce')
            
            if df[year].max() < 2000:
                df[year] = (df[year] * 1000).round()
                
        except Exception as e:
            print(f"Hata {year} yılı dönüşümünde: {e}")

df_melted = df.melt(
    id_vars=["Üniversite Adı"],
    value_vars=[col for col in [2020, 2021, 2022, 2023, 2024] if col in df.columns],
    var_name="Yıl",
    value_name="Başarı Sırası"
).dropna()

df_melted["Yıl"] = df_melted["Yıl"].astype(str)

RENK_KOYU = '#f46e16'
RENK_ORTA = '#f46e16'
RENK_ARKAPLAN = '#f6f6e9'
YAZI_RENGI = '#000000'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.facecolor'] = RENK_ARKAPLAN
plt.rcParams['axes.titlesize'] = 22
fig, ax = plt.subplots(figsize=(14, 8), facecolor=RENK_ARKAPLAN)
sns.set_style("ticks", {'axes.grid': False})

boxplot = sns.boxplot(
    x="Yıl",
    y="Başarı Sırası",
    data=df_melted,
    ax=ax,
    width=0.5,
    boxprops=dict(facecolor=RENK_ORTA, edgecolor=RENK_KOYU, linewidth=2, alpha=0.8),
    whiskerprops=dict(color=RENK_KOYU, linewidth=2),
    medianprops=dict(color=RENK_KOYU, linewidth=2.5),
    capprops=dict(color=RENK_KOYU, linewidth=2),
    flierprops=dict(marker='D',
                   markersize=6,
                   markerfacecolor=RENK_ARKAPLAN,
                   markeredgecolor=RENK_KOYU)
)

ax.set_title("YBS Bölümlerinin Kontejanları (2020-2024)", 
            fontweight='bold', 
            color=YAZI_RENGI,
            pad=20)

ax.invert_yaxis()

plt.xticks(fontsize=12, color=YAZI_RENGI)
plt.yticks(fontsize=12, color=YAZI_RENGI)

for spine in ax.spines.values():
    spine.set_color(RENK_KOYU)
    spine.set_linewidth(1.5)

ax.grid(False)

plt.tight_layout()
plt.savefig('ybs_basari_siralama_boxplot_sade.png', dpi=300, bbox_inches='tight')
plt.show()