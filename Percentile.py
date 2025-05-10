import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RENK_KOYU = '#f46e16'
RENK_ORTA = '#f46e16'
RENK_ARKAPLAN = '#f6f6e9'
YAZI_RENGI = '#000000'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.facecolor'] = RENK_ARKAPLAN
plt.rcParams['axes.titlesize'] = 18

data = {
    "Üniversite": [
        "BOĞAZİÇİ ÜNİVERSİTESİ",
        "MARMARA ÜNİVERSİTESİ",
        "İSTANBUL ÜNİVERSİTESİ",
        "GAZİ ÜNİVERSİTESİ",
        "DOKUZEYLÜL ÜNİVERSİTESİ",
        "AKSARAY ÜNİVERSİTESİ"
    ],
    "2020": [0.117, 0.660, 0.518, 2.241, 6.032, 25.194],
    "2021": [0.068, 0.227, 0.215, 0.811, 3.830, 17.581],
    "2022": [0.045, 0.116, 0.255, 0.772, 2.532, 10.981],
    "2023": [0.027, 0.140, None, None, 1.420, 8.802],
    "2024": [0.030, None, None, None, 1.536, 7.829]
}

df_clean = pd.DataFrame(data).set_index("Üniversite")
df_sorted = df_clean.sort_values(by="2024", na_position='last')
ilk_5 = df_sorted.head(5).drop("AKSARAY ÜNİVERSİTESİ", errors='ignore')
aksaray = df_clean[df_clean.index.str.contains("AKSARAY", case=False)]

fig, ax = plt.subplots(figsize=(14, 8), facecolor=RENK_ARKAPLAN)
sns.set_style("ticks", {'axes.grid': False})

ax.set_title("YBS BÖLÜMLERİNİN ÖĞRENCİ ALDIĞI YÜZDELİK DİLİMLER\nİLK 5 VE AKSARAY ÜNİVERSİTESİ",
             fontweight='bold',
             color=YAZI_RENGI,
             pad=20,
             loc='center')

university_colors = {
    "BOĞAZİÇİ ÜNİVERSİTESİ": "#f46e16",
    "MARMARA ÜNİVERSİTESİ": "#C45100",
    "İSTANBUL ÜNİVERSİTESİ": "#EB895F",
    "GAZİ ÜNİVERSİTESİ": "#F0A787",
    "DOKUZEYLÜL ÜNİVERSİTESİ": "#F5C4AF",
    "AKSARAY ÜNİVERSİTESİ": "#73361C"
}

for uni in ilk_5.index:
    values = ilk_5.loc[uni]
    years = ilk_5.columns
    valid_years = [year for year, val in zip(years, values) if pd.notna(val)]
    valid_values = [val for val in values if pd.notna(val)]

    ax.plot(valid_years, valid_values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=uni,
            color=university_colors[uni])

    if uni == "BOĞAZİÇİ ÜNİVERSİTESİ":
        for year, val in zip(valid_years, valid_values):
            ax.annotate(f"%{val:.3f}",
                        (year, val),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center',
                        fontsize=10,
                        weight='bold',
                        color=university_colors[uni],
                        bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2'))
    
    if uni == "DOKUZEYLÜL ÜNİVERSİTESİ":
        for year, val in zip(valid_years, valid_values):
            ax.annotate(f"%{val:.3f}",
                        (year, val),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center',
                        fontsize=10,
                        weight='bold',
                        color=university_colors[uni],
                        bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2'))

if not aksaray.empty:
    values = aksaray.values.flatten()
    years = aksaray.columns
    valid_years = [year for year, val in zip(years, values) if pd.notna(val)]
    valid_values = [val for val in values if pd.notna(val)]

    ax.plot(valid_years, valid_values,
            marker="X",
            linestyle="--",
            color=university_colors["AKSARAY ÜNİVERSİTESİ"],
            linewidth=3,
            markersize=12,
            label="AKSARAY ÜNİVERSİTESİ")

    for year, val in zip(valid_years, valid_values):
        ax.annotate(f"%{val:.3f}",
                    (year, val),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center',
                    fontsize=10,
                    weight='bold',
                    color=university_colors["AKSARAY ÜNİVERSİTESİ"],
                    bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2'))

ax.set_xlabel("Yıl", fontsize=14, color=YAZI_RENGI)
ax.set_ylabel("Yüzdelik Dilim (%)", fontsize=14, color=YAZI_RENGI)
ax.tick_params(axis='both', which='major', labelsize=12, colors=YAZI_RENGI)

for spine in ax.spines.values():
    spine.set_color(RENK_KOYU)
    spine.set_linewidth(1.5)

ax.legend(bbox_to_anchor=(1.05, 1),
          loc="upper left",
          frameon=True,
          facecolor=RENK_ARKAPLAN,
          edgecolor=RENK_KOYU,
          fontsize=11)

y_max = df_clean.max().max()
ax.set_ylim(0, y_max * 1.1)

ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.set_ylabel("Sıralama (Daha iyi →)", fontsize=14, color=YAZI_RENGI)
ax2.invert_yaxis()
ax2.set_yticks([])

ax.grid(False)

plt.tight_layout()
plt.show()