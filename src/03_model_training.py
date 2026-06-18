import pandas as pd
import numpy as np
import pickle
import os
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

def entrenar_modelos():
    print("Iniciando entrenamiento de modelos...")
    df = pd.read_csv("data/data_processed.csv")
    
    # Preparar X e y (quitamos columnas no predictivas y contaminantes actuales para evitar data leakage)
    cols_to_drop = ['Fecha', 'Estacion', 'Region', 'Estado', 'PM2.5', 'PM10', 'O3', 'NO2', 'SO2', 'CO', 'Mala_Calidad_Aire']
    X = df.drop(columns=cols_to_drop, errors='ignore')
    y = df['Mala_Calidad_Aire']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Escalar
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Definir Modelos
    modelos = {
        "Regresión Logística": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
        "Red Neuronal (MLP)": MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=500, random_state=42)
    }
    
    resultados = {}
    matrices = {}
    importancias = {}
    
    os.makedirs("models", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    for nombre, modelo in modelos.items():
        print(f"Entrenando {nombre}...")
        modelo.fit(X_train_scaled, y_train)
        
        y_pred = modelo.predict(X_test_scaled)
        y_prob = modelo.predict_proba(X_test_scaled)[:, 1] if hasattr(modelo, "predict_proba") else y_pred
        
        resultados[nombre] = {
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred),
            "Recall": recall_score(y_test, y_pred),
            "F1_Score": f1_score(y_test, y_pred),
            "AUC_ROC": roc_auc_score(y_test, y_prob)
        }
        
        matrices[nombre] = confusion_matrix(y_test, y_pred).tolist()
        
        with open(f"models/{nombre.replace(' ', '_').replace('(', '').replace(')', '')}.pkl", "wb") as f:
            pickle.dump(modelo, f)
            
        if hasattr(modelo, "feature_importances_"):
            importancias[nombre] = dict(zip(X.columns, modelo.feature_importances_.tolist()))

    with open("output/metricas.json", "w") as f:
        json.dump(resultados, f, indent=4)
    with open("output/matrices.json", "w") as f:
        json.dump(matrices, f, indent=4)
    with open("output/importancias.json", "w") as f:
        json.dump(importancias, f, indent=4)
        
    print("¡Modelos entrenados!")

if __name__ == "__main__":
    entrenar_modelos()
