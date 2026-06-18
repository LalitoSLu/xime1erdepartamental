import json
import os
import pandas as pd

def generar_dashboard():
    print("Generando Dashboard HTML Power BI UI (Ultra Detallado)...")
    
    with open("output/metricas.json", "r") as f:
        metricas = json.loads(f.read())
    with open("output/importancias.json", "r") as f:
        importancias = json.loads(f.read())

    df = pd.read_csv("data/data_processed.csv")
    total_malos = int(df['Mala_Calidad_Aire'].sum())
    total_buenos = int(len(df) - total_malos)
    pct_buenos = (total_buenos / len(df)) * 100
    
    # Generar barras horizontales en HTML para "Importancia de Variables" (Copia exacta de la imagen)
    xgb_imp = importancias["XGBoost"]
    sorted_imp = sorted([{"k": k, "v": v} for k, v in xgb_imp.items()], key=lambda x: x["v"], reverse=True)[:5]
    max_imp = sorted_imp[0]["v"]
    
    horiz_bars_html = ""
    for item in sorted_imp:
        width_pct = (item["v"] / max_imp) * 100
        val_display = f"{(item['v']*100):.1f}%"
        horiz_bars_html += f"""
        <div class="horiz-bar-row">
            <div class="horiz-bar-label">{item['k'][:15]}</div>
            <div class="horiz-bar-track">
                <div class="horiz-bar-fill" style="width: {width_pct}%;">
                    <span class="horiz-bar-value">{val_display}</span>
                </div>
            </div>
        </div>
        """

    # Generar tabla inferior (Copia exacta de la imagen)
    tabla_html = ""
    for nombre, mets in metricas.items():
        acc = mets["Accuracy"] * 100
        f1 = mets["F1_Score"] * 100
        rec = mets["Recall"] * 100
        
        # Ajustar anchos visuales para que se vean como la imagen (no llegar hasta el borde si es 100%)
        w_acc = acc * 0.9
        w_f1 = f1 * 0.9
        
        tabla_html += f"""
        <tr class="data-row">
            <td style="color:#d1d5db;">{nombre.replace(' (MLP)','')}</td>
            <td>
                <div class="tbl-bar-track">
                    <div class="tbl-bar-fill blue" style="width: {w_acc}%;">
                        <span>{acc:.1f}%</span>
                    </div>
                </div>
            </td>
            <td>
                <div class="tbl-bar-track">
                    <div class="tbl-bar-fill green" style="width: {w_f1}%;">
                        <span>{f1:.1f}%</span>
                    </div>
                </div>
            </td>
            <td class="td-pink-cell"><div class="pink-box">{rec:.0f}%</div></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Power BI Experience Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&family=Montserrat:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-body: #1b2028;
            --bg-sidebar: #171a1f;
            --bg-card: #272e38;
            --blue: #2563eb;
            --green: #10b981;
            --pink: #e11d48;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}
        
        * {{ box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            margin: 0;
            display: flex;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* SIDEBAR (Sin botones inútiles) */
        .sidebar {{
            width: 60px; min-width: 60px;
            background-color: var(--bg-sidebar);
            display: flex; flex-direction: column; align-items: center;
            padding: 20px 0; gap: 20px;
            box-shadow: 2px 0 10px rgba(0,0,0,0.3); z-index: 10;
        }}
        .icon-btn {{
            width: 40px; height: 40px; border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            color: var(--text-muted); font-size: 1.2rem; cursor: pointer;
        }}
        .icon-btn.chevron {{ cursor: default; font-size: 1.4rem; }}
        .icon-btn.active {{ background: rgba(37, 99, 235, 0.2); color: #60a5fa; }}

        .main-content {{
            flex: 1; padding: 25px 35px; width: calc(100% - 60px);
        }}

        /* HEADER */
        .header-container {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;
        }}
        .header-title {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700; font-size: 1.2rem; letter-spacing: 6px; color: #fff;
        }}
        .header-logo {{
            font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1rem; color: #fff; display: flex; align-items: center; gap: 5px;
        }}
        .header-logo span {{ color: #0ea5e9; font-style: italic; }}

        /* GRIDS */
        .grid-3-top {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-bottom: 25px; width: 100%; }}
        .grid-3-bottom {{ display: grid; grid-template-columns: 1fr 1.2fr 2fr; gap: 25px; width: 100%; }}

        /* CARDS */
        .card {{
            background-color: var(--bg-card); border-radius: 12px; padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); display: flex; flex-direction: column;
        }}

        /* TOP KPI GRADIENT BOXES */
        .kpi-box {{
            border-radius: 12px; padding: 20px;
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 20px; box-shadow: inset 0 0 40px rgba(0,0,0,0.2);
        }}
        .kpi-box.blue {{ background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); }}
        .kpi-box.green {{ background: linear-gradient(135deg, #064e3b 0%, #047857 100%); }}
        .kpi-box.pink {{ background: linear-gradient(135deg, #4c0519 0%, #be123c 100%); }}
        
        .kpi-info {{ display: flex; align-items: center; gap: 15px; }}
        .kpi-icon {{
            width: 35px; height: 35px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            background: rgba(0,0,0,0.2); font-size: 0.9rem; font-weight: bold; color: rgba(255,255,255,0.7);
        }}
        .kpi-text h2 {{ margin: 0; font-size: 2rem; font-weight: 700; color: #fff; letter-spacing: 1px; }}
        .kpi-text p {{ margin: 5px 0 0 0; font-size: 0.75rem; color: rgba(255,255,255,0.7); letter-spacing: 2px; text-transform: uppercase; }}

        .sparkline-wrapper {{ width: 100px; height: 50px; position: relative; }}
        .chart-wrapper-top {{ width: 100%; height: 160px; position: relative; }}
        .chart-wrapper-bottom {{ width: 100%; height: 250px; position: relative; }}

        .panel-title {{
            font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
            margin-bottom: 25px; color: #fff; letter-spacing: 1px;
        }}

        /* HORIZONTAL BARS HTML (Middle Bottom Panel) */
        .horiz-bar-row {{ display: flex; align-items: center; margin-bottom: 12px; gap: 15px; font-size: 0.75rem; }}
        .horiz-bar-label {{ width: 110px; text-align: right; color: #d1d5db; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .horiz-bar-track {{ flex: 1; height: 22px; background: transparent; position: relative; }}
        .horiz-bar-fill {{
            height: 100%; background-color: var(--green); display: flex; justify-content: flex-end; align-items: center;
            padding-right: 10px; font-weight: 700; color: #fff; text-shadow: 0 0 2px rgba(0,0,0,0.5); border-radius: 2px;
        }}

        /* TABLE (Right Bottom Panel) */
        .custom-table {{ width: 100%; border-collapse: collapse; font-size: 0.75rem; color: #e2e8f0; }}
        .custom-table th {{
            text-align: left; padding: 10px 5px 15px 5px; color: var(--text-main); font-weight: 600;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .custom-table td {{ padding: 10px 5px; border-bottom: 1px solid rgba(255,255,255,0.03); }}
        
        .tbl-bar-track {{ width: 100%; height: 22px; background: transparent; position: relative; }}
        .tbl-bar-fill {{
            height: 100%; display: flex; align-items: center; justify-content: center;
            font-weight: 600; color: #fff; font-size: 0.7rem; text-shadow: 0 0 3px rgba(0,0,0,0.6); border-radius: 2px;
        }}
        .tbl-bar-fill.blue {{ background-color: #60a5fa; }}
        .tbl-bar-fill.green {{ background-color: #34d399; }}
        
        .td-pink-cell {{ padding: 0 !important; width: 50px; border-bottom: 1px solid rgba(255,255,255,0.03); }}
        .pink-box {{
            background-color: #f472b6; color: #fff; text-align: center; font-weight: 700; 
            padding: 10px 0; height: 100%; display: flex; align-items: center; justify-content: center;
        }}
        
        .total-row td {{ border-top: 1px solid rgba(255,255,255,0.2); font-weight: 700; padding-top: 15px; border-bottom: none; }}
    </style>
</head>
<body>

    <div class="sidebar">
        <!-- Chevron (No click) -->
        <div class="icon-btn chevron">》</div>
        <!-- Solo el botón que sirve (Dashboard) -->
        <div class="icon-btn active" title="Dashboard">📊</div>
    </div>

    <div class="main-content">
        <div class="header-container">
            <div class="header-title">PREDICCIÓN x CALIDAD x AIRE</div>
            <div class="header-logo">POWER BI <span>EXPERIENCE</span></div>
        </div>

        <!-- TOP SECTION -->
        <div class="grid-3-top">
            <div class="card">
                <div class="kpi-box blue">
                    <div class="kpi-info">
                        <div class="kpi-icon">⚙</div>
                        <div class="kpi-text">
                            <h2 id="xgb-auc">0%</h2>
                            <p>XGBOOST AUC</p>
                        </div>
                    </div>
                    <div class="sparkline-wrapper"><canvas id="sparkBlue"></canvas></div>
                </div>
                <div class="chart-wrapper-top"><canvas id="barBlue"></canvas></div>
            </div>

            <div class="card">
                <div class="kpi-box green">
                    <div class="kpi-info">
                        <div class="kpi-icon">🌲</div>
                        <div class="kpi-text">
                            <h2 id="rf-auc">0%</h2>
                            <p>RANDOM FOREST AUC</p>
                        </div>
                    </div>
                    <div class="sparkline-wrapper"><canvas id="sparkGreen"></canvas></div>
                </div>
                <div class="chart-wrapper-top"><canvas id="barGreen"></canvas></div>
            </div>

            <div class="card">
                <div class="kpi-box pink">
                    <div class="kpi-info">
                        <div class="kpi-icon">🧠</div>
                        <div class="kpi-text">
                            <h2 id="mlp-auc">0%</h2>
                            <p>RED NEURONAL AUC</p>
                        </div>
                    </div>
                    <div class="sparkline-wrapper"><canvas id="sparkPink"></canvas></div>
                </div>
                <div class="chart-wrapper-top"><canvas id="barPink"></canvas></div>
            </div>
        </div>

        <!-- BOTTOM SECTION -->
        <div class="grid-3-bottom">
            <!-- Donut -->
            <div class="card">
                <div class="panel-title">PROPORCIÓN DE EPISODIOS</div>
                <div class="chart-wrapper-bottom">
                    <canvas id="donutChart"></canvas>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: var(--text-muted); font-size: 0.75rem;">
                        <span style="font-size: 1.8rem; color: #fff; display: block; font-weight:700;">{pct_buenos:.0f}%</span>
                        Aceptable
                    </div>
                </div>
            </div>

            <!-- Horizontal Bars -->
            <div class="card">
                <div class="panel-title">IMPORTANCIA POR VARIABLE</div>
                <div style="width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; padding-right: 15px;">
                    {horiz_bars_html}
                </div>
            </div>

            <!-- Table -->
            <div class="card">
                <div class="panel-title">ANÁLISIS POR MODELO (MÉTRICAS CLAVE)</div>
                <table class="custom-table" style="margin-top: 10px;">
                    <thead>
                        <tr>
                            <th>Modelos</th>
                            <th style="width: 35%;">Accuracy</th>
                            <th style="width: 35%;">F1-Score</th>
                            <th style="width: 15%; text-align: center;">Recall%</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tabla_html}
                        <tr class="total-row">
                            <td style="color:#fff;">Regresión Log.</td>
                            <td style="text-align: center;">--</td>
                            <td style="text-align: center;">--</td>
                            <td style="text-align: center;">--</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const metricas = {json.dumps(metricas)};
        
        document.getElementById('xgb-auc').innerText = (metricas["XGBoost"]["AUC_ROC"] * 100).toFixed(1) + "%";
        document.getElementById('rf-auc').innerText = (metricas["Random Forest"]["AUC_ROC"] * 100).toFixed(1) + "%";
        document.getElementById('mlp-auc').innerText = (metricas["Red Neuronal (MLP)"]["AUC_ROC"] * 100).toFixed(1) + "%";

        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Segoe UI', Tahoma, sans-serif";
        Chart.defaults.maintainAspectRatio = false;
        Chart.defaults.responsive = true;

        const metricsLabels = ['Accuracy', 'Precision', 'Recall', 'F1', 'AUC'];

        // SPARK LINES (Línea con gradiente hacia abajo y punto rojo/verde al final)
        function createSparkline(ctxId, color, pointColor) {{
            const ctx = document.getElementById(ctxId).getContext('2d');
            new Chart(ctx, {{
                type: 'line',
                data: {{ 
                    labels: ['1','2','3','4','5'], 
                    datasets: [{{ 
                        data: [60, 65, 80, 85, 65], 
                        borderColor: color, 
                        borderWidth: 2, 
                        tension: 0.3, 
                        pointRadius: [0, 0, 0, 0, 4], // Punto solo al final
                        pointBackgroundColor: pointColor 
                    }}] 
                }},
                options: {{ 
                    plugins: {{ legend: {{ display: false }}, tooltip: {{ enabled: false }} }},
                    scales: {{ x: {{ display: false }}, y: {{ display: false, min: 40, max: 100 }} }},
                    layout: {{ padding: {{ right: 5, top: 5, bottom: 5 }} }} 
                }}
            }});
        }}
        createSparkline('sparkBlue', '#60a5fa', '#f87171');
        createSparkline('sparkGreen', '#34d399', '#f87171');
        createSparkline('sparkPink', '#f472b6', '#f87171');

        // TOP BAR CHARTS (Eje Y con líneas punteadas)
        function createTopBar(ctxId, color, dataVals) {{
            const ctx = document.getElementById(ctxId).getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{ labels: metricsLabels, datasets: [{{ data: dataVals, backgroundColor: color, barThickness: 18 }}] }},
                options: {{ 
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{ 
                        y: {{ 
                            beginAtZero: true, max: 100, 
                            ticks: {{ stepSize: 25, callback: v => v+'%', font: {{ size: 10 }} }}, 
                            grid: {{ color: 'rgba(255,255,255,0.08)', borderDash: [4, 4], drawBorder: false }} 
                        }}, 
                        x: {{ 
                            grid: {{ display: false }},
                            ticks: {{ font: {{ size: 10 }} }}
                        }} 
                    }} 
                }}
            }});
        }}
        
        const mXgb = metricas["XGBoost"];
        const mRf = metricas["Random Forest"];
        const mMlp = metricas["Red Neuronal (MLP)"];
        
        createTopBar('barBlue', '#2563eb', [mXgb.Accuracy*100, mXgb.Precision*100, mXgb.Recall*100, mXgb.F1_Score*100, mXgb.AUC_ROC*100]);
        createTopBar('barGreen', '#10b981', [mRf.Accuracy*100, mRf.Precision*100, mRf.Recall*100, mRf.F1_Score*100, mRf.AUC_ROC*100]);
        createTopBar('barPink', '#e11d48', [mMlp.Accuracy*100, mMlp.Precision*100, mMlp.Recall*100, mMlp.F1_Score*100, mMlp.AUC_ROC*100]);

        // DONUT CHART
        const ctxDonut = document.getElementById('donutChart').getContext('2d');
        new Chart(ctxDonut, {{
            type: 'doughnut',
            data: {{
                labels: ['Aceptable', 'Mala Calidad'],
                datasets: [{{ data: [{total_buenos}, {total_malos}], backgroundColor: ['#2563eb', 'rgba(37, 99, 235, 0.2)'], borderWidth: 0 }}]
            }},
            options: {{ cutout: '80%', plugins: {{ legend: {{ display: false }} }} }}
        }});

    </script>
</body>
</html>"""

    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("¡Dashboard de demostración Power BI Ultra Detallado generado!")

if __name__ == "__main__":
    generar_dashboard()
