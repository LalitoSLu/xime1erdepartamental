import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generar_datos():
    print("Generando datos sintéticos realistas con SINAICA, CONAGUA, INEGI y SEMARNAT...")
    np.random.seed(42)
    
    estaciones = [f"Estacion_{i:02d}" for i in range(1, 51)]
    regiones = ["Norte", "Centro", "Sur"]
    estados = [f"Estado_{i}" for i in range(1, 11)]
    
    fecha_inicio = datetime(2023, 1, 1)
    fechas = [fecha_inicio + timedelta(days=i) for i in range(365)]
    
    # 1. Datos Urbanos (INEGI)
    datos_urbanos = []
    for est in estaciones:
        region = np.random.choice(regiones)
        estado = np.random.choice(estados)
        poblacion = np.random.randint(50000, 5000000)
        parque_vehicular = int(poblacion * np.random.uniform(0.2, 0.6))
        datos_urbanos.append({
            "Estacion": est,
            "Estado": estado,
            "Region": region,
            "Poblacion": poblacion,
            "Parque_Vehicular": parque_vehicular
        })
    df_urbanos = pd.DataFrame(datos_urbanos)
    
    # 2. Datos de Emisiones (SEMARNAT)
    datos_semarnat = []
    for estado in estados:
        emisiones_industriales = np.random.randint(1000, 50000)
        datos_semarnat.append({
            "Estado": estado,
            "Emisiones_Industriales_Ton": emisiones_industriales
        })
    df_semarnat = pd.DataFrame(datos_semarnat)
    
    # 3. Datos de Calidad del Aire (SINAICA) y Clima (CONAGUA)
    registros_aire = []
    registros_clima = []
    
    for est in estaciones:
        # Base contaminantes según la población
        pob_factor = df_urbanos[df_urbanos['Estacion'] == est]['Poblacion'].values[0] / 5000000
        estado_est = df_urbanos[df_urbanos['Estacion'] == est]['Estado'].values[0]
        ind_factor = df_semarnat[df_semarnat['Estado'] == estado_est]['Emisiones_Industriales_Ton'].values[0] / 50000
        
        for fecha in fechas:
            mes = fecha.month
            temp_base = 25 if 4 <= mes <= 9 else 15
            temp = temp_base + np.random.normal(0, 5)
            
            prob_lluvia = 0.6 if 6 <= mes <= 9 else 0.1
            lluvia = 1 if np.random.rand() < prob_lluvia else 0
            humedad = 60 + np.random.normal(0, 10) + (20 if lluvia else 0)
            
            invierno_factor = 1.5 if mes in [11, 12, 1, 2] else 1.0
            lluvia_factor = 0.5 if lluvia else 1.0
            
            pm25 = max(5, np.random.normal(20, 10) * invierno_factor * lluvia_factor * (1 + pob_factor + ind_factor))
            pm10 = pm25 * np.random.uniform(1.5, 2.5)
            o3 = max(10, np.random.normal(50, 15) * (temp / 20))
            no2 = max(5, np.random.normal(15, 8) * (1 + pob_factor))
            so2 = max(2, np.random.normal(8, 4) * (1 + ind_factor))
            co = max(1, np.random.normal(3, 1) * (1 + pob_factor))
            
            registros_aire.append({
                "Fecha": fecha,
                "Estacion": est,
                "PM2.5": pm25,
                "PM10": pm10,
                "O3": o3,
                "NO2": no2,
                "SO2": so2,
                "CO": co
            })
            
            registros_clima.append({
                "Fecha": fecha,
                "Estacion": est,
                "Temperatura": temp,
                "Humedad": humedad,
                "Lluvia": lluvia
            })
            
    df_aire = pd.DataFrame(registros_aire)
    df_clima = pd.DataFrame(registros_clima)
    
    os.makedirs("data", exist_ok=True)
    df_aire.to_csv("data/calidad_aire.csv", index=False)
    df_clima.to_csv("data/clima.csv", index=False)
    df_urbanos.to_csv("data/datos_urbanos.csv", index=False)
    df_semarnat.to_csv("data/emisiones_semarnat.csv", index=False)
    
    print("¡Datos generados exitosamente!")

if __name__ == "__main__":
    generar_datos()
