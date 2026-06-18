import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import numpy as np

def generar_graficas_eda():
    print("Generando gráficas estáticas para el reporte (EDA y Modelos)...")
    os.makedirs("output/plots", exist_ok=True)
    
    # 1. Cargar datos
    df = pd.read_csv("data/data_processed.csv")
    
    # Configuración de estilo global
    plt.style.use('dark_background')
    sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#0d1117", "figure.facecolor": "#0d1117", "text.color": "white", "axes.labelcolor": "white", "xtick.color": "white", "ytick.color": "white"})
    
    # 2. Matriz de Correlación
    print("-> Generando Matriz de Correlación...")
    plt.figure(figsize=(12, 8))
    # Seleccionamos solo variables numéricas relevantes
    cols_num = ['PM2.5', 'PM10', 'O3', 'NO2', 'Temperatura', 'Humedad', 'Mala_Calidad_Aire']
    corr = df[cols_num].corr()
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", center=0, 
                linewidths=1, linecolor="#0d1117", cbar_kws={"shrink": .8})
    plt.title("Matriz de Correlación de Contaminantes y Clima", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig("output/plots/matriz_correlacion.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Distribución de la Variable Objetivo
    print("-> Generando Distribución de Variable Objetivo...")
    plt.figure(figsize=(8, 6))
    ax = sns.countplot(data=df, x='Mala_Calidad_Aire', palette=['#10b981', '#ef4444'])
    plt.title("Distribución: Calidad Aceptable (0) vs Mala Calidad (1)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Estado de Calidad del Aire")
    plt.ylabel("Cantidad de Registros (Días)")
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig("output/plots/distribucion_objetivo.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Serie de Tiempo de Contaminantes (Muestra)
    print("-> Generando Serie Temporal...")
    plt.figure(figsize=(14, 6))
    df_sample = df[df['Estacion'] == 'Estacion_01'].sort_values('Fecha')
    plt.plot(pd.to_datetime(df_sample['Fecha']), df_sample['PM2.5'], color='#38bdf8', label='PM2.5')
    plt.axhline(y=45, color='#ef4444', linestyle='--', label='Límite Norma (45 µg/m³)')
    plt.title("Evolución Anual de PM2.5 - Estación 01", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Fecha")
    plt.ylabel("Concentración (µg/m³)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/plots/serie_temporal_pm25.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Importancia de Variables de XGBoost (Cargando de JSON)
    print("-> Generando Gráfica de Importancia de Variables...")
    with open("output/importancias.json", "r") as f:
        importancias = json.load(f)
    
    xgb_imp = importancias.get("XGBoost", {})
    df_imp = pd.DataFrame(list(xgb_imp.items()), columns=["Variable", "Importancia"]).sort_values(by="Importancia", ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_imp, x="Importancia", y="Variable", palette="viridis")
    plt.title("Importancia de Variables (Modelo XGBoost)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Importancia Relativa")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("output/plots/importancia_xgboost.png", dpi=300, bbox_inches='tight')
    plt.close()

    print("¡Gráficas generadas exitosamente en 'output/plots/'!")

if __name__ == "__main__":
    generar_graficas_eda()
