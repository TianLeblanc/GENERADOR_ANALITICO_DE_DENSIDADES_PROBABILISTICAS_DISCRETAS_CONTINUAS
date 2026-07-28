import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Importamos tu lógica matemática central intacta
from Generadores.GeneradorUniforme import GeneradorUniforme
from Analisis.AnalizadorEstadistico import AnalizadorEstadistico

# Configuración inicial de la página web (Modo ancho)
st.set_page_config(
    page_title="Analizador Estadístico de Uniformes",
    page_icon="📊",
    layout="wide"
)

# Estilos CSS personalizados para un diseño oscuro moderno y elegante
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

st.title("📊 Analizador Estadístico: Distribuciones Uniformes")
st.markdown("Generación estocástica, validación analítica y gráficas teóricas de densidad y probabilidad.")

# --- BARRA LATERAL DE CONFIGURACIÓN ---
st.sidebar.header("⚙️ Configuración del Experimento")

tipo_distribucion = st.sidebar.selectbox(
    "Selecciona la Distribución",
    ["Continua U(0,1)", "Discreta Entera"]
)

cantidad = st.sidebar.number_input("Cantidad de números (n)", value=500, min_value=10, step=50)
nivel_confianza = st.sidebar.slider("Nivel de Confianza (%)", min_value=80, max_value=99, value=95) / 100.0

# Parámetros condicionales
min_val, max_val = 0.0, 1.0
min_d, max_d = 1, 10

if "Continua" in tipo_distribucion:
    with st.sidebar.expander("Parámetros de Escala (Continua)"):
        min_val = st.number_input("Límite Inferior (a)", value=0.0)
        max_val = st.number_input("Límite Superior (b)", value=1.0)
else:
    with st.sidebar.expander("Parámetros de Rango (Discreta)"):
        min_d = st.number_input("Valor Mínimo Entero", value=1, step=1)
        max_d = st.number_input("Valor Máximo Entero", value=10, step=1)

# --- BOTÓN DE EJECUCIÓN ---
if st.sidebar.button("🚀 Generar y Evaluar", type="primary"):
    
    # 1. Generación de datos puros convertidos estrictamente a listas de Python nativas
    if "Continua" in tipo_distribucion:
        datos_brutos = GeneradorUniforme.generar_continua(int(cantidad), float(min_val), float(max_val))
        if max_val != min_val:
            datos_para_pruebas = [(x - min_val) / (max_val - min_val) for x in datos_brutos]
        else:
            datos_para_pruebas = datos_brutos
        datos_visibles = [float(x) for x in datos_brutos]
    else:
        datos_enteros = GeneradorUniforme.generar_discreta(int(cantidad), int(min_d), int(max_d))
        datos_visibles = [float(x) for x in datos_enteros]
        amplitud = float((max_d - min_d) + 1)
        datos_para_pruebas = [(x - min_d) / amplitud for x in datos_visibles]

    # 2. Ejecución de tu Analizador Estadístico
    analizador = AnalizadorEstadistico(nivel_confianza=nivel_confianza)
    reporte = analizador.evaluar_generador(
        numeros=datos_para_pruebas,
        nombre_generador=f"Uniforme {tipo_distribucion}",
        parametros={"n": cantidad, "confianza": nivel_confianza}
    )

    # --- TARJETAS DE MÉTRICAS SUPERIORES ---
    st.success("¡Pruebas ejecutadas con éxito!")
    col1, col2, col3, col4 = st.columns(4)

    def render_metric_card(col, prueba, prefijo):
        estado = "✅ PASÓ" if prueba.pasa_validacion else "❌ FALLÓ"
        val = f"{prefijo} {prueba.valor_calculado}" if isinstance(prueba.valor_calculado, (int, float)) else prueba.valor_calculado
        col.metric(label=f"{prueba.nombre_prueba} ({estado})", value=val, delta=f"Crítico: {prueba.valor_critico_tabla}")

    render_metric_card(col1, reporte.prueba_media, "Z =")
    render_metric_card(col2, reporte.prueba_varianza, "Chi² =")
    render_metric_card(col3, reporte.prueba_ks, "D =")
    render_metric_card(col4, reporte.prueba_independencia, "Z =")

    st.markdown("---")

    # --- TABLERO DE GRÁFICAS ANALÍTICAS (AHORA CON 4 PESTAÑAS) ---
    st.subheader("📈 Tablero de Gráficas Analíticas y de Validación")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📉 1. Distribución Teórica", 
        "📊 2. Histograma de Frecuencias", 
        "🔄 3. Prueba de Independencia (Serial)", 
        "📈 4. Kolmogorov-Smirnov (Acumulada)"
    ])

    template_grafico = "plotly_dark"

    with tab1:
        st.markdown("### Gráfica Teórica de la Distribución")
        fig_teo = go.Figure()
        if "Continua" in tipo_distribucion:
            # Función de Densidad Uniforme Continua f(x) = 1 / (b - a)
            b_menos_a = max_val - min_val if max_val != min_val else 1.0
            altura = 1.0 / b_menos_a
            x_vals = [min_val, max_val]
            y_vals = [altura, altura]
            fig_teo.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'U({min_val}, {max_val})', line=dict(color='#3B82F6', width=4)))
            fig_teo.update_layout(xaxis_title="X", yaxis_title="Densidad f(x)", template=template_grafico)
        else:
            # Función de Probabilidad Uniforme Discreta
            valores_unicos = list(range(int(min_d), int(max_d) + 1))
            prob_teorica_val = 1.0 / len(valores_unicos)
            y_vals = [prob_teorica_val] * len(valores_unicos)
            fig_teo.add_trace(go.Bar(x=valores_unicos, y=y_vals, marker_color='#3B82F6', name='Probabilidad P(X=x)'))
            fig_teo.update_layout(xaxis_title="Valores Enteros", yaxis_title="Probabilidad", template=template_grafico)

        fig_teo.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_teo, use_container_width=True)

    with tab2:
        st.markdown("### Histograma de Frecuencias de la Muestra")
        if "Continua" in tipo_distribucion:
            fig_hist = px.histogram(x=list(datos_visibles), nbins=20, labels={'x': 'Intervalos (U_i)', 'y': 'Frecuencia'}, template=template_grafico)
        else:
            fig_hist = px.histogram(x=list(datos_visibles), nbins=int((max_d - min_d) + 1), labels={'x': 'Valores Enteros', 'y': 'Frecuencia'}, template=template_grafico)
        
        fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', bargap=0.1)
        st.plotly_chart(fig_hist, use_container_width=True)

    with tab3:
        st.markdown("### Gráfica de Dispersión $U_i$ vs $U_{i+1}$ (Independencia)")
        if len(datos_visibles) > 1:
            ui = list(datos_visibles[:-1])
            ui_1 = list(datos_visibles[1:])
            fig_disp = px.scatter(x=ui, y=ui_1, labels={'x': 'U_i', 'y': 'U_{i+1}'}, template=template_grafico)
            fig_disp.update_traces(marker=dict(size=8, color='#3B82F6', opacity=0.8))
            fig_disp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_disp, use_container_width=True)
        else:
            st.warning("Se requieren más datos para graficar la dispersión.")

    with tab4:
        st.markdown("### Ajuste de Probabilidad Acumulada (Kolmogorov-Smirnov)")
        datos_vis = reporte.visuales_ks if hasattr(reporte, 'visuales_ks') else reporte.datos_visuales_ks
        if datos_vis and len(datos_vis.numeros_ordenados) > 0:
            fig_ks = go.Figure()
            fig_ks.add_trace(go.Scatter(x=list(datos_vis.numeros_ordenados), y=list(datos_vis.probabilidad_real), mode='lines', name='Empírica F(x)', line=dict(color='#3B82F6', width=3)))
            fig_ks.add_trace(go.Scatter(x=list(datos_vis.numeros_ordenados), y=list(datos_vis.probabilidad_teorica), mode='lines', name='Teórica F_0(x)', line=dict(color='#EF4444', width=2, dash='dash')))
            fig_ks.update_layout(xaxis_title="X", yaxis_title="Probabilidad Acumulada", template=template_grafico, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_ks, use_container_width=True)
        else:
            st.info("No hay datos de K-S disponibles para graficar.")

    st.markdown("---")

    # --- SECCIÓN DE LA TABLA DE NÚMEROS GENERADOS ---
    st.subheader("📋 Tabla de Números Generados")
    st.markdown(f"Mostrando los **{len(datos_visibles)}** números generados por la distribución:")
    
    tabla_datos = [{"Índice": i + 1, "Valor Generado": val} for i, val in enumerate(datos_visibles)]
    st.dataframe(tabla_datos, use_container_width=True, height=300)

else:
    st.info("👈 Configura los parámetros en el panel lateral izquierdo y presiona **'Generar y Evaluar'** para iniciar la simulación.")