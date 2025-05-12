import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

file_paths = {
    2020: r"C:\Users\alper\OneDrive\Masaüstü\Ders Notları\3.Sınıf\Veri Gorsellestirme\2020 YBS Puanları.xlsx",
    2021: r"C:\Users\alper\OneDrive\Masaüstü\Ders Notları\3.Sınıf\Veri Gorsellestirme\2021 YBS Puanları.xlsx",
    2022: r"C:\Users\alper\OneDrive\Masaüstü\Ders Notları\3.Sınıf\Veri Gorsellestirme\2022 YBS Puanları.xlsx",
    2023: r"C:\Users\alper\OneDrive\Masaüstü\Ders Notları\3.Sınıf\Veri Gorsellestirme\2023 YBS Puanları.xlsx",
    2024: r"C:\Users\alper\OneDrive\Masaüstü\Ders Notları\3.Sınıf\Veri Gorsellestirme\2024 YBS Puanları.xlsx"
}

all_dfs = []

for year, file_path in file_paths.items():
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            
            kontenjan_column = None
            for col in df.columns:
                if "Kontenjan" in str(col):
                    kontenjan_column = col
                    break
            
            if kontenjan_column:
                df_selected = df[["Üniversite Adı", kontenjan_column]].copy()
                
                df_selected[kontenjan_column] = (
                    df_selected[kontenjan_column]
                    .astype(str)
                    .str.replace("\n", "", regex=False)
                    .str.replace(" ", "", regex=False)
                    .str.strip()
                )
                
                df_selected[kontenjan_column] = df_selected[kontenjan_column].replace(
                    ["nan", "——", "—", "-", "Dolmadı", "NA", "", "None"], np.nan
                )
                
                df_selected[kontenjan_column] = pd.to_numeric(df_selected[kontenjan_column], errors='coerce')
                
                df_selected["Yıl"] = year
                
                df_selected.rename(columns={kontenjan_column: "Kontenjan"}, inplace=True)
                
                all_dfs.append(df_selected)
                
                print(f"{year} yılı verisi başarıyla işlendi. Satır sayısı: {len(df_selected)}")
            else:
                print(f"{year} yılı için Kontenjan sütunu bulunamadı.")
        
        except Exception as e:
            print(f"Hata {year} yılı dosyasında: {e}")
    else:
        print(f"{year} yılı dosyası bulunamadı: {file_path}")

if all_dfs:
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    combined_df = combined_df.dropna(subset=["Kontenjan"])
    
    print(f"Toplam veri satır sayısı: {len(combined_df)}")
    
    RENK_KOYU = '#f46e16'
    RENK_ORTA = '#f46e16'
    RENK_ARKAPLAN = '#f6f6e9'
    YAZI_RENGI = '#000000'
    
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.facecolor'] = RENK_ARKAPLAN
    plt.rcParams['axes.titlesize'] = 22
    
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=RENK_ARKAPLAN)
    sns.set_style("ticks", {'axes.grid': False})
    
    combined_df["Yıl"] = combined_df["Yıl"].astype(str)
    
    boxplot = sns.boxplot(
        x="Yıl",
        y="Kontenjan",
        data=combined_df,
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
    
    ax.set_title("YBS Bölümlerinin Kontenjanları (2020-2024)",
                fontweight='bold',
                color=YAZI_RENGI,
                pad=20)
    
    ax.set_ylabel("Kontenjan Sayısı", fontsize=14, color=YAZI_RENGI)
    ax.set_xlabel("Yıl", fontsize=14, color=YAZI_RENGI)
    
    plt.xticks(fontsize=12, color=YAZI_RENGI)
    plt.yticks(fontsize=12, color=YAZI_RENGI)
    
    for spine in ax.spines.values():
        spine.set_color(RENK_KOYU)
        spine.set_linewidth(1.5)
    
    ax.grid(False)
    
    yearly_means = combined_df.groupby("Yıl")["Kontenjan"].mean().round(1)
    
    for i, year in enumerate(sorted(combined_df["Yıl"].unique())):
        mean_val = yearly_means[year]
        ax.text(i, mean_val, f"Ort: {mean_val}", 
                horizontalalignment='center', 
                size=10, 
                color=YAZI_RENGI,
                weight='bold',
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
    
    plt.tight_layout()
    plt.savefig('ybs_kontenjan_boxplot.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nYıllara Göre Kontenjan İstatistikleri:")
    stats = combined_df.groupby("Yıl")["Kontenjan"].agg(['count', 'mean', 'median', 'min', 'max']).round(1)
    print(stats)
    
else:
    print("İşlenecek veri bulunamadı.")