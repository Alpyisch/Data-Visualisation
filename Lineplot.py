import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = r"C:\Users\alper\OneDrive\Masaüstü\Ders Notları\3.Sınıf\Veri Gorsellestirme\ybs_taban_puanlari.xlsx"
df = pd.read_excel(file_path)

print("Orijinal veri örneği:")
print(df.head())
print("\nSütun tipleri:", df.dtypes)

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

        print(f"\n{year} yılı için benzersiz değerler:")
        print(df[year].unique()[:10])

        try:
            df[year] = pd.to_numeric(df[year], errors='coerce')

            if df[year].max() < 2000:
                df[year] = (df[year] * 1000).round()

        except Exception as e:
            print(f"Hata {year} yılı dönüşümünde: {e}")

aksaray_df = df[df['Üniversite Adı'].str.contains('Aksaray', case=False, na=False)]

if len(aksaray_df) > 0:
    print("\nAksaray Üniversitesi verileri bulundu:")
    print(aksaray_df)
else:
    print("\nAksaray Üniversitesi verisi bulunamadı!")

df_melted = df.melt(
    id_vars=["Üniversite Adı"],
    value_vars=[col for col in [2020, 2021, 2022, 2023, 2024] if col in df.columns],
    var_name="Yıl",
    value_name="Başarı Sırası"
).dropna()

yearly_avg = df_melted.groupby("Yıl")["Başarı Sırası"].mean().reset_index()
yearly_std = df_melted.groupby("Yıl")["Başarı Sırası"].std().reset_index()

aksaray_data = df_melted[df_melted['Üniversite Adı'].str.contains('Aksaray', case=False, na=False)]
aksaray_yearly = aksaray_data.groupby("Yıl")["Başarı Sırası"].mean().reset_index()

theme_colors = {
    'background': '#f6f6e9',
    'line': '#f46e16',
    'fill': '#e69b6a',
    'text': '#4A4A4A',
    'grid': '#CCCCCC',
    'aksaray': '#73361C'  # Aksaray için renk tonu
}

plt.style.use('seaborn-v0_8')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.titlesize': 22,
    'axes.labelsize': 14,
    'axes.facecolor': theme_colors['background']
})

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(theme_colors['background'])

ax.plot(
    yearly_avg["Yıl"],
    yearly_avg["Başarı Sırası"],
    color=theme_colors['line'],
    marker='o',
    markersize=12,
    linewidth=3.5,
    markerfacecolor='white',
    markeredgewidth=2,
    label='Genel Ortalama Başarı Sırası'
)

ax.fill_between(
    yearly_avg["Yıl"],
    yearly_avg["Başarı Sırası"] - yearly_std["Başarı Sırası"],
    yearly_avg["Başarı Sırası"] + yearly_std["Başarı Sırası"],
    color=theme_colors['fill'],
    alpha=0.15,
    label='Standart Sapma'
)

if not aksaray_yearly.empty:
    ax.plot(
        aksaray_yearly["Yıl"],
        aksaray_yearly["Başarı Sırası"],
        color=theme_colors['aksaray'],
        marker='s',
        markersize=12,
        linewidth=3.5,
        markerfacecolor='white',
        markeredgewidth=2,
        label='Aksaray Üniversitesi'
    )

    for year, value in zip(aksaray_yearly["Yıl"], aksaray_yearly["Başarı Sırası"]):
        ax.text(year, value - -15000, f'{int(value):,}',
                ha='center', va='top',
                color=theme_colors['aksaray'],
                fontsize=12,
                fontweight='bold')

ax.set_title("YBS Sıralamaları (2020-2024)", 
            fontweight='bold', 
            color=theme_colors['text'],
            pad=20)

ax.set_xlabel("Yıl", color=theme_colors['text'], labelpad=15)
ax.set_ylabel("Başarı Sırası", color=theme_colors['text'], labelpad=15)

available_years = sorted(yearly_avg["Yıl"].unique())
ax.set_xticks(available_years)
ax.set_xticklabels(available_years, color=theme_colors['text'])
ax.tick_params(axis='y', colors=theme_colors['text'])
ax.invert_yaxis()

ax.grid(False)

for spine in ax.spines.values():
    spine.set_color(theme_colors['grid'])

legend = ax.legend(
    loc='upper right',
    frameon=True,
    framealpha=0.9,
    facecolor='white',
    edgecolor=theme_colors['grid']
)

for year, value in zip(yearly_avg["Yıl"], yearly_avg["Başarı Sırası"]):
    ax.text(year, value + -7000, f'{int(value):,}',
            ha='center', va='bottom',
            color=theme_colors['line'],
            fontsize=12,
            fontweight='bold')

plt.tight_layout()
plt.savefig('ybs_aksaray_karsilastirma.png', dpi=300, bbox_inches='tight')
plt.show()

if not aksaray_yearly.empty:
    print("\nAksaray Üniversitesi YBS - Başarı Sıralaması İstatistikleri:")
    for year, row in aksaray_yearly.iterrows():
        print(f"{int(row['Yıl'])} yılı: {int(row['Başarı Sırası']):,}")
    
    print("\nGenel Ortalama ile Karşılaştırma:")
    for year in available_years:
        aks_val = aksaray_yearly[aksaray_yearly['Yıl'] == year]['Başarı Sırası'].values
        avg_val = yearly_avg[yearly_avg['Yıl'] == year]['Başarı Sırası'].values
        
        if len(aks_val) > 0 and len(avg_val) > 0:
            diff = aks_val[0] - avg_val[0]
            better = "daha iyi" if diff < 0 else "daha kötü"
            print(f"{year}: Aksaray, ortalamadan {abs(int(diff)):,} sıra {better}")