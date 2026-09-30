"""
Dashboard de Calidad del Aire - Bogotá 2025
============================================
Construido con Streamlit + Pandas + Plotly.

Ejecutar con:
    streamlit run app.py

El archivo de datos "datos_calidad_aire_bogota_2025.csv" debe estar en la misma
carpeta que este script (o puedes cargarlo manualmente desde la barra lateral).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

# ----------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Calidad del Aire - Bogotá 2025",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILENAME = "datos_calidad_aire_bogota_2025.csv"

# Rangos oficiales de referencia IBOCA (Índice Bogotano de Calidad del Aire)
IBOCA_BANDS = [
    (0, 50, "Buena", "#00B050"),
    (50, 100, "Aceptable", "#FFFF00"),
    (100, 150, "Regular", "#FFA500"),
    (150, 200, "Mala", "#FF0000"),
    (200, 300, "Muy mala", "#7030A0"),
    (300, 1000, "Peligrosa", "#800000"),
]


def clasificar_iboca(valor: float) -> str:
    if pd.isna(valor):
        return "Sin dato"
    for low, high, label, _ in IBOCA_BANDS:
        if low <= valor < high:
            return label
    return "Peligrosa"


# ----------------------------------------------------------------------------
# CARGA DE DATOS (con caché para no releer el CSV en cada interacción)
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner="Cargando datos de calidad del aire...")
def load_data(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"])
    df["Fecha"] = df["Fecha_Hora"].dt.date
    df["Hora"] = df["Fecha_Hora"].dt.hour
    df["Mes"] = df["Fecha_Hora"].dt.month
    df["DiaSemana"] = df["Fecha_Hora"].dt.day_name()
    df["Categoria_IBOCA"] = df["IBOCA"].apply(clasificar_iboca)
    return df


st.sidebar.title("🌤️ Filtros del Dashboard")

local_path = Path(__file__).parent / DATA_FILENAME
uploaded_file = None

if local_path.exists():
    data_source = local_path
else:
    st.sidebar.warning(f"No se encontró '{DATA_FILENAME}' junto al script.")
    uploaded_file = st.sidebar.file_uploader("Sube el archivo CSV", type=["csv"])
    data_source = uploaded_file

if data_source is None:
    st.title("🌤️ Calidad del Aire - Bogotá 2025")
    st.info("Carga el archivo CSV desde la barra lateral para comenzar.")
    st.stop()

df = load_data(data_source)

# ----------------------------------------------------------------------------
# FILTROS - BARRA LATERAL
# ----------------------------------------------------------------------------
fecha_min, fecha_max = df["Fecha"].min(), df["Fecha"].max()
rango_fechas = st.sidebar.date_input(
    "Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max,
)
if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
    fecha_ini, fecha_fin = rango_fechas
else:
    fecha_ini, fecha_fin = fecha_min, fecha_max

estaciones_disponibles = sorted(df["Estacion"].unique())
estaciones_sel = st.sidebar.multiselect(
    "Estaciones de monitoreo",
    options=estaciones_disponibles,
    default=estaciones_disponibles,
)

contaminante_sel = st.sidebar.radio(
    "Contaminante",
    options=sorted(df["Contaminante"].unique()),
    horizontal=True,
)

metrica_sel = st.sidebar.selectbox(
    "Métrica a analizar",
    options=["Concentracion", "NowCast", "IBOCA"],
    index=2,
    help="Concentracion: medición cruda (µg/m³). NowCast: promedio ponderado reciente. "
         "IBOCA: índice de calidad del aire de Bogotá.",
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Fuente: Red de Monitoreo de Calidad del Aire de Bogotá (RMCAB). "
    "Datos horarios PM10 y PM2.5, año 2025."
)

# Aplicar filtros
mask = (
    (df["Fecha"] >= fecha_ini)
    & (df["Fecha"] <= fecha_fin)
    & (df["Estacion"].isin(estaciones_sel))
    & (df["Contaminante"] == contaminante_sel)
)
df_f = df.loc[mask].copy()

if df_f.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# ----------------------------------------------------------------------------
# ENCABEZADO Y KPIs
# ----------------------------------------------------------------------------
st.title("🌤️ Dashboard de Calidad del Aire - Bogotá 2025")
st.caption(
    f"Contaminante: **{contaminante_sel}** · Métrica: **{metrica_sel}** · "
    f"Periodo: **{fecha_ini}** a **{fecha_fin}** · "
    f"{len(estaciones_sel)} estación(es) seleccionada(s)"
)

col1, col2, col3, col4 = st.columns(4)

promedio = df_f[metrica_sel].mean()
maximo = df_f[metrica_sel].max()
pct_datos_validos = df_f[metrica_sel].notna().mean() * 100

fila_max = df_f.loc[df_f[metrica_sel].idxmax()] if df_f[metrica_sel].notna().any() else None
estacion_max = fila_max["Estacion"] if fila_max is not None else "N/A"

peor_estacion = (
    df_f.groupby("Estacion")[metrica_sel].mean().sort_values(ascending=False).index[0]
    if df_f[metrica_sel].notna().any()
    else "N/A"
)

col1.metric(f"Promedio {metrica_sel}", f"{promedio:,.1f}")
col2.metric(f"Máximo registrado", f"{maximo:,.1f}", help=f"Estación: {estacion_max}")
col3.metric("Estación más contaminada (promedio)", peor_estacion)
col4.metric("Datos válidos", f"{pct_datos_validos:,.1f}%")

st.markdown("---")

# ----------------------------------------------------------------------------
# SERIE DE TIEMPO
# ----------------------------------------------------------------------------
st.subheader("📈 Evolución temporal")

df_serie = (
    df_f.groupby(["Fecha_Hora", "Estacion"])[metrica_sel]
    .mean()
    .reset_index()
)

fig_serie = px.line(
    df_serie,
    x="Fecha_Hora",
    y=metrica_sel,
    color="Estacion",
    labels={"Fecha_Hora": "Fecha", metrica_sel: metrica_sel},
)
fig_serie.update_layout(
    height=450,
    legend_title_text="Estación",
    hovermode="x unified",
)

if metrica_sel == "IBOCA":
    for low, high, label, color in IBOCA_BANDS:
        fig_serie.add_hrect(
            y0=low, y1=high, fillcolor=color, opacity=0.06, line_width=0
        )

st.plotly_chart(fig_serie, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------------
# COMPARATIVO ENTRE ESTACIONES + DISTRIBUCIÓN
# ----------------------------------------------------------------------------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🏭 Promedio por estación")
    df_estacion = (
        df_f.groupby("Estacion")[metrica_sel]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_bar = px.bar(
        df_estacion,
        x=metrica_sel,
        y="Estacion",
        orientation="h",
        color=metrica_sel,
        color_continuous_scale="YlOrRd",
    )
    fig_bar.update_layout(height=500, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    st.subheader("📊 Distribución de valores")
    fig_hist = px.histogram(
        df_f,
        x=metrica_sel,
        color="Estacion",
        nbins=40,
        opacity=0.7,
    )
    fig_hist.update_layout(height=500, legend_title_text="Estación")
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------------
# PATRONES: HORA DEL DÍA Y DÍA DE LA SEMANA
# ----------------------------------------------------------------------------
st.subheader("🕒 Patrones horarios y semanales")

col_c, col_d = st.columns(2)

with col_c:
    df_hora = df_f.groupby("Hora")[metrica_sel].mean().reset_index()
    fig_hora = px.line(
        df_hora, x="Hora", y=metrica_sel, markers=True,
        title="Promedio por hora del día",
    )
    fig_hora.update_layout(height=400)
    st.plotly_chart(fig_hora, use_container_width=True)

with col_d:
    orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    nombres_es = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo",
    }
    df_dia = df_f.groupby("DiaSemana")[metrica_sel].mean().reindex(orden_dias).reset_index()
    df_dia["DiaSemana"] = df_dia["DiaSemana"].map(nombres_es)
    fig_dia = px.bar(
        df_dia, x="DiaSemana", y=metrica_sel,
        title="Promedio por día de la semana",
        color=metrica_sel, color_continuous_scale="Blues",
    )
    fig_dia.update_layout(height=400)
    st.plotly_chart(fig_dia, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------------
# MAPA DE CALOR: ESTACIÓN x MES
# ----------------------------------------------------------------------------
st.subheader("🔥 Mapa de calor: Estación vs. Mes")

meses_es = {
    1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic",
}
df_heat = (
    df_f.groupby(["Estacion", "Mes"])[metrica_sel]
    .mean()
    .reset_index()
)
df_heat["MesNombre"] = df_heat["Mes"].map(meses_es)
pivot = df_heat.pivot(index="Estacion", columns="MesNombre", values=metrica_sel)
pivot = pivot.reindex(columns=[meses_es[m] for m in sorted(df_heat["Mes"].unique())])

fig_heat = go.Figure(
    data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="YlOrRd",
        colorbar=dict(title=metrica_sel),
    )
)
fig_heat.update_layout(height=500)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------------
# CLASIFICACIÓN IBOCA (solo si la métrica seleccionada es IBOCA)
# ----------------------------------------------------------------------------
if metrica_sel == "IBOCA":
    st.subheader("🚦 Distribución por categoría IBOCA")
    orden_cat = [b[2] for b in IBOCA_BANDS] + ["Sin dato"]
    colores_cat = {b[2]: b[3] for b in IBOCA_BANDS}
    colores_cat["Sin dato"] = "#CCCCCC"

    conteo_cat = df_f["Categoria_IBOCA"].value_counts().reindex(orden_cat).dropna().reset_index()
    conteo_cat.columns = ["Categoria", "Registros"]

    fig_cat = px.pie(
        conteo_cat,
        names="Categoria",
        values="Registros",
        color="Categoria",
        color_discrete_map=colores_cat,
        hole=0.4,
    )
    fig_cat.update_layout(height=450)
    st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------------
# TABLA DE DATOS DETALLADA
# ----------------------------------------------------------------------------
st.subheader("📋 Datos detallados")
st.dataframe(
    df_f[["Fecha_Hora", "Estacion", "Contaminante", "Concentracion", "NowCast", "IBOCA"]]
    .sort_values("Fecha_Hora", ascending=False),
    use_container_width=True,
    height=350,
)

csv_export = df_f.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Descargar datos filtrados (CSV)",
    data=csv_export,
    file_name="calidad_aire_filtrado.csv",
    mime="text/csv",
)
