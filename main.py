import os
import subprocess

def run_pipeline():
    print("=========================================")
    print("=== PIPELINE DE CALIDAD DEL AIRE MEXICO ===")
    print("=========================================")
    
    # 1. Generar datos
    print("\n[1/4] Generando datos...")
    os.system("python src/01_data_generator.py")
    
    # 2. Preprocesamiento
    print("\n[2/4] Preprocesando datos...")
    os.system("python src/02_preprocessing.py")
    
    # 3. Entrenamiento
    print("\n[3/4] Entrenando modelos de ML...")
    os.system("python src/03_model_training.py")
    
    # 4. Generar Gráficas EDA
    print("\n[4/5] Generando gráficas EDA estáticas...")
    os.system("python src/06_generar_eda_plots.py")
    
    # 5. Generar Dashboard HTML
    print("\n[5/5] Generando el Dashboard HTML Premium de Demostración...")
    os.system("python src/05_export_html.py")
    
    print("\n[INFO] TODO LISTO! Ve a la carpeta del proyecto y abre el archivo 'dashboard.html' con tu navegador.")

if __name__ == "__main__":
    run_pipeline()
