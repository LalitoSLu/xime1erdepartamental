import pandas as pd
import numpy as np

def preprocesar_datos():
    print("Iniciando preprocesamiento e integración...")
    
    df_aire = pd.read_csv("data/calidad_aire.csv", parse_dates=["Fecha"])
    df_clima = pd.read_csv("data/clima.csv", parse_dates=["Fecha"])
    df_urbanos = pd.read_csv("data/datos_urbanos.csv")
    df_semarnat = pd.read_csv("data/emisiones_semarnat.csv")
    
    # Unir (Merge)
    df_merged = pd.merge(df_aire, df_clima, on=["Fecha", "Estacion"])
    df_merged = pd.merge(df_merged, df_urbanos, on="Estacion")
    df_merged = pd.merge(df_merged, df_semarnat, on="Estado")
    
    df_merged.sort_values(["Estacion", "Fecha"], inplace=True)
    
    print("Calculando variables del día anterior y promedios móviles...")
    
    # 1. Contaminantes del día anterior (Exigido en rúbrica)
    for col in ['PM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO']:
        df_merged[f'{col}_ayer'] = df_merged.groupby('Estacion')[col].shift(1)
        
    # 2. Promedios de los últimos 3 días (rezagos adicionales)
    for col in ['PM2.5', 'PM10', 'Temperatura']:
        df_merged[f'{col}_ma3'] = df_merged.groupby('Estacion')[col].transform(lambda x: x.shift(1).rolling(window=3, min_periods=1).mean())
    
    df_merged.bfill(inplace=True)
    
    # Densidad Vehicular per capita
    df_merged['Densidad_Vehicular_Pob'] = df_merged['Parque_Vehicular'] / df_merged['Poblacion']
    
    # Variable Objetivo: 1 = Mala Calidad (Si PM2.5 > 45 o PM10 > 75)
    df_merged['Mala_Calidad_Aire'] = ((df_merged['PM2.5'] > 45) | (df_merged['PM10'] > 75)).astype(int)
    
    df_merged['Mes'] = df_merged['Fecha'].dt.month
    
    df_merged.to_csv("data/data_processed.csv", index=False)
    
    print(f"Preprocesamiento terminado. Total de registros: {len(df_merged)}")

if __name__ == "__main__":
    preprocesar_datos()
