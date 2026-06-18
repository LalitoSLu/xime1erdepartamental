import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuración Súper Genial del Dashboard
st.set_page_config(page_title="AI Air Quality Predictor", layout="wide", page_icon="🌬️")

# Estilos CSS Personalizados para UI Premium
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3 { color: #58a6ff; font-family: 'Inter', sans-serif; font-weight: 700; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    div[data-testid="stSidebar"] { background-color: #010409; border-right: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

st.title("🌬️ IA Predictiva: Calidad del Aire en México")
st.markdown("Dashboard interactivo para monitorear y predecir episodios de mala calidad del aire basados en datos climáticos y urbanos.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/data_processed.csv")
    with open("output/metricas.json", "r") as f:
        metrics = json.load(f)
    with open("output/matrices.json", "r") as f:
        matrices = json.load(f)
    with open("output/importancias.json", "r") as f:
        importances = json.load(f)
    return df, metrics, matrices, importances

try:
    df, metrics, matrices, importances = load_data()
    
    # ---- SIDEBAR ----
    st.sidebar.header("⚙️ Configuración")
    seccion = st.sidebar.radio("Navegación", ["Análisis Exploratorio (EDA)", "Evaluación de Modelos", "Predicción en Vivo"])
    
    if seccion == "Análisis Exploratorio (EDA)":
        st.header("📊 Análisis Exploratorio y Distribución de Contaminantes")
        
        # KPIs Superiores
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Estaciones Monitoreadas", df['Estacion'].nunique())
        col2.metric("Días Registrados", df['Fecha'].nunique())
        col3.metric("Episodios de Riesgo", int(df['Mala_Calidad_Aire'].sum()))
        col4.metric("PM2.5 Promedio Nacional", f"{df['PM2.5'].mean():.2f} µg/m³")
        
        st.divider()
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Tendencia de PM2.5 a lo largo del tiempo")
            df_temp = df.sample(2000).sort_values('Fecha')
            fig_line = px.line(df_temp, x='Fecha', y='PM2.5', color='Region', 
                              color_discrete_sequence=px.colors.qualitative.Vivid,
                              template="plotly_dark")
            st.plotly_chart(fig_line, use_container_width=True)
            
        with col_chart2:
            st.subheader("Correlación: Temperatura vs Ozono (O3)")
            fig_scatter = px.scatter(df.sample(1000), x='Temperatura', y='O3', color='Mala_Calidad_Aire',
                                    color_continuous_scale="Reds", template="plotly_dark",
                                    hover_data=['Estacion', 'Region'])
            st.plotly_chart(fig_scatter, use_container_width=True)
            
    elif seccion == "Evaluación de Modelos":
        st.header("🤖 Rendimiento de los Modelos de Inteligencia Artificial")
        
        # Mostrar Métricas en Tabla
        df_metrics = pd.DataFrame(metrics).T
        
        # Formatear como porcentajes
        st.dataframe(df_metrics.style.format("{:.2%}").background_gradient(cmap='Blues'))
        
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.subheader("🏆 Comparativa de AUC-ROC")
            fig_bar = px.bar(df_metrics, y='AUC_ROC', text_auto='.2%', color=df_metrics.index,
                            template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_m2:
            st.subheader("🧠 Importancia de Variables (Random Forest)")
            imp_rf = pd.DataFrame(list(importances['Random_Forest'].items()), columns=['Variable', 'Importancia']).sort_values('Importancia', ascending=True)
            fig_imp = px.bar(imp_rf, x='Importancia', y='Variable', orientation='h', template="plotly_dark", color='Importancia', color_continuous_scale="Teal")
            st.plotly_chart(fig_imp, use_container_width=True)
            
        st.subheader("🧩 Matrices de Confusión")
        cols = st.columns(len(matrices))
        for i, (nombre, matrix) in enumerate(matrices.items()):
            with cols[i]:
                fig_cm = px.imshow(matrix, text_auto=True, color_continuous_scale='Blues', template='plotly_dark',
                                  labels=dict(x="Predicción", y="Realidad"), title=nombre)
                fig_cm.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig_cm, use_container_width=True)

    elif seccion == "Predicción en Vivo":
        st.header("⚡ Simulador Predictivo en Tiempo Real")
        st.markdown("Modifica las variables para predecir si habrá mala calidad del aire hoy.")
        
        with st.form("simulador"):
            col1, col2, col3 = st.columns(3)
            with col1:
                pm25_ayer = st.slider("PM2.5 Ayer (µg/m³)", 0, 150, 30)
                pm10_ayer = st.slider("PM10 Ayer (µg/m³)", 0, 200, 50)
            with col2:
                temp_ayer = st.slider("Temperatura Ayer (°C)", 0, 40, 25)
                temp = st.slider("Temperatura Hoy (°C)", 0, 40, 26)
            with col3:
                lluvia = st.selectbox("¿Llovió?", [0, 1])
                humedad = st.slider("Humedad (%)", 0, 100, 60)
            
            poblacion = st.number_input("Población Local", value=1000000)
            vehiculos = st.number_input("Parque Vehicular", value=300000)
            mes = st.slider("Mes del Año", 1, 12, 6)
            
            submitted = st.form_submit_button("🧪 Predecir Calidad del Aire")
            
            if submitted:
                import pickle
                try:
                    with open("models/XGBoost.pkl", "rb") as f:
                        modelo = pickle.load(f)
                    # Simular las mismas variables que X
                    #['Temperatura', 'Humedad', 'Lluvia', 'Poblacion', 'Parque_Vehicular', 'PM2.5_ma3', 'PM10_ma3', 'Temperatura_ma3', 'Densidad_Vehicular_Pob', 'Mes']
                    densidad = vehiculos / poblacion
                    input_data = pd.DataFrame([{
                        'Temperatura': temp,
                        'Humedad': humedad,
                        'Lluvia': lluvia,
                        'Poblacion': poblacion,
                        'Parque_Vehicular': vehiculos,
                        'PM2.5_ma3': pm25_ayer,
                        'PM10_ma3': pm10_ayer,
                        'Temperatura_ma3': temp_ayer,
                        'Densidad_Vehicular_Pob': densidad,
                        'Mes': mes
                    }])
                    
                    # Escalar (simplificado para el demo, normalmente cargaríamos el scaler)
                    # Para XGBoost no es estricto el scaler
                    prediccion = modelo.predict(input_data)[0]
                    prob = modelo.predict_proba(input_data)[0][1]
                    
                    st.divider()
                    if prediccion == 1:
                        st.error(f"🚨 ALERTA: Probabilidad del {prob:.1%} de registrar MALA calidad del aire.")
                    else:
                        st.success(f"✅ AIRE LIMPIO: Probabilidad de riesgo es baja ({prob:.1%}).")
                except Exception as e:
                    st.warning("Asegúrate de entrenar los modelos primero ejecutando los scripts.")
                    st.code(str(e))
except Exception as e:
    st.warning("⚠️ No se encontraron los datos. Por favor ejecuta `main.py` para generar los datos y modelos.")
