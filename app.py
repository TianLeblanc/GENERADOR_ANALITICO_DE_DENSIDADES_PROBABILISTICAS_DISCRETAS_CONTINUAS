import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from Generadores.GeneradorUniforme import GeneradorUniforme
from Analisis.AnalizadorEstadistico import AnalizadorEstadistico

st.set_page_config(
    page_title="Analizador Estadístico - Uniforme Discreta",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stSidebar {
        background-color: #161B22 !important;
    }
    div[data-testid="stMetric"] {
        background-color: #1F2937;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1F2937;
        border-radius: 8px 8px 0px 0px;
        color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Analizador Estadístico: Distribución Uniforme Discreta")
st.markdown("Generación estocástica y validación analítica estricta para variables discretas.")

# --- BARRA LATERAL ---
st.sidebar.header("⚙️ Configuración del Experimento")

cantidad = st.sidebar.number_input("Cantidad de números (n)", value=500, min_value=10, step=50)
nivel_confianza = st.sidebar.slider("Nivel de Confianza (%)", min_value=80, max_value=99, value=95) / 100.0

with st.sidebar.expander("Parámetros de Rango (Discreta)", expanded=True):
    min_d = st.number_input("Valor Mínimo Entero (a)", value=1, step=1)
    max_d = st.number_input("Valor Máximo Entero (b)", value=10, step=1)

# --- BOTÓN DE EJECUCIÓN ---
if st.sidebar.button("🚀 Generar y Evaluar", type="primary"):

    datos_enteros = GeneradorUniforme.generar_discreta(int(cantidad), int(min_d), int(max_d))
    datos_visibles = [float(x) for x in datos_enteros]

    analizador = AnalizadorEstadistico(
        nivel_confianza=nivel_confianza, 
        min_d=int(min_d), 
        max_d=int(max_d)
    )

    reporte = analizador.evaluar_generador(
        numeros=datos_visibles,
        nombre_generador="Uniforme Discreta",
        parametros={"n": cantidad, "confianza": nivel_confianza, "min": min_d, "max": max_d}
    )

    st.success("¡Pruebas ejecutadas con éxito!")
    col1, col2, col3, col4 = st.columns(4)

    def render_metric_card(col, prueba, prefijo):
        estado = "✅ PASÓ" if prueba.pasa_validacion else "❌ FALLÓ"
        val = f"{prefijo} {prueba.valor_calculado}" if isinstance(prueba.valor_calculado, (int, float)) else prueba.valor_calculado

        col.markdown(f"""
            <div style="
                background-color: #1F2937;
                padding: 16px;
                border-radius: 12px;
                border: 1px solid #374151;
                margin-bottom: 10px;
                height: 165px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            ">
                <div>
                    <div style="font-size: 0.85em; color: #D1D5DB; font-weight: 600; margin-bottom: 6px;">
                        {prueba.nombre_prueba} ({estado})
                    </div>
                    <div style="font-size: 1.3em; font-weight: bold; color: #FFFFFF; line-height: 1.2;">
                        {val}
                    </div>
                </div>
                <div style="font-size: 0.85em; color: #9CA3AF; border-top: 1px solid #374151; padding-top: 4px; margin-top: 4px;">
                    Crítico: {prueba.valor_critico_tabla}
                </div>
            </div>
        """, unsafe_allow_html=True)

    render_metric_card(col1, reporte.resultado_media, "Z =")
    render_metric_card(col2, reporte.resultado_varianza, "Chi² =")
    render_metric_card(col3, reporte.resultado_ks, "Chi² =")  # Cambiamos el prefijo a Chi²
    render_metric_card(col4, reporte.resultado_independencia, "Z =")
    st.markdown("---")

    # --- TABS DE GRÁFICAS ---
    st.subheader("📈 Tablero de Gráficas Analíticas")
    
    tab1, tab2, tab3 = st.tabs([
        "📉 1. Distribución Teórica", 
        "📊 2. Histograma de Frecuencias", 
        "🔄 3. Prueba de Independencia (Serial)"
    ])

    template_grafico = "plotly_dark"

    with tab1:
        st.markdown("### Gráfica Teórica de Probabilidad Discreta P(X = x)")
        valores_unicos = list(range(int(min_d), int(max_d) + 1))
        prob_teorica_val = 1.0 / len(valores_unicos)
        y_vals = [prob_teorica_val] * len(valores_unicos)

        fig_teo = go.Figure()
        fig_teo.add_trace(go.Bar(
            x=valores_unicos,
            y=y_vals,
            marker_color='#3B82F6',
            marker_line_color='#93C5FD',
            marker_line_width=2,
            opacity=0.9,
            name='P(X = x)'
        ))
        fig_teo.update_layout(
            xaxis_title="Valores Enteros Discretos",
            yaxis_title="Probabilidad P(x)",
            template=template_grafico,
            bargap=0.25,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#1F2937'),
            yaxis=dict(showgrid=True, gridcolor='#1F2937')
        )
        st.plotly_chart(fig_teo, use_container_width=True)

    with tab2:
        st.markdown("### Histograma de Frecuencias de la Muestra")
        fig_hist = px.histogram(
            x=list(datos_visibles), 
            nbins=int((max_d - min_d) + 1), 
            labels={'x': 'Valores Enteros', 'y': 'Frecuencia'}, 
            template=template_grafico
        )
        fig_hist.update_traces(marker_color='#10B981', marker_line_color='#34D399', marker_line_width=1)
        fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', bargap=0.1)
        st.plotly_chart(fig_hist, use_container_width=True)

    with tab3:
        st.markdown("### Gráfica de Dispersión $X_i$ vs $X_{i+1}$ (Independencia)")
        if len(datos_visibles) > 1:
            ui = list(datos_visibles[:-1])
            ui_1 = list(datos_visibles[1:])
            fig_disp = px.scatter(x=ui, y=ui_1, labels={'x': 'X_i', 'y': 'X_{i+1}'}, template=template_grafico)
            fig_disp.update_traces(marker=dict(size=8, color='#8B5CF6', opacity=0.7))
            fig_disp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_disp, use_container_width=True)
        else:
            st.warning("Se requieren más datos para graficar la dispersión.")

    st.markdown("---")

    st.subheader("📋 Tabla de Números Generados")
    tabla_datos = [{"Índice": i + 1, "Valor Generado": int(val)} for i, val in enumerate(datos_visibles)]
    st.dataframe(tabla_datos, use_container_width=True, height=300)

else:
    st.info("👈 Configura los parámetros en el panel lateral izquierdo y presiona **'Generar y Evaluar'** para iniciar la simulación.")