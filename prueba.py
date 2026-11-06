import streamlit as st
import time
import altair as alt

# Inicializa la conexión usando st.connection
conn = st.connection("mysql", type="sql")

# Consulta los últimos 10 datos
df = conn.query(
    "SELECT id, voltaje, irradiancia FROM muestras ORDER BY id DESC LIMIT 10;", ttl=0
)

# Ordenar los datos por id en orden ascendente para graficar correctamente
df_sorted = df.sort_values(by="id")

# Crear una nueva columna para representar el índice como "Cantidad de Datos"
df_sorted["muestras"] = range(1, len(df_sorted) + 1)

st.title("Tabla de Muestras")
# Mostrar tabla de datos
st.dataframe(df_sorted)

# Cálculo de estadísticas para voltaje
ultimo_voltaje = df_sorted['voltaje'].iloc[-1]
min_voltaje = df_sorted['voltaje'].min()
max_voltaje = df_sorted['voltaje'].max()
prom_voltaje = df_sorted['voltaje'].mean()

# Cálculo de estadísticas para irradiancia
ultima_irradiancia = df_sorted['irradiancia'].iloc[-1]
min_irradiancia = df_sorted['irradiancia'].min()
max_irradiancia = df_sorted['irradiancia'].max()
prom_irradiancia = df_sorted['irradiancia'].mean()

# Mostrar métricas en columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Estadísticas de Voltaje")
    st.metric("Último valor", f"{ultimo_voltaje:.2f} V")
    st.metric("Mínimo", f"{min_voltaje:.2f} V")
    st.metric("Máximo", f"{max_voltaje:.2f} V")
    st.metric("Promedio", f"{prom_voltaje:.2f} V")

with col2:
    st.subheader("Estadísticas de Irradiancia")
    st.metric("Último valor", f"{ultima_irradiancia:.2f} W/m²")
    st.metric("Mínimo", f"{min_irradiancia:.2f} W/m²")
    st.metric("Máximo", f"{max_irradiancia:.2f} W/m²")
    st.metric("Promedio", f"{prom_irradiancia:.2f} W/m²")

st.title("Gráfico de Voltaje")
# Graficar los últimos datos agregados
chart = (
    alt.Chart(df_sorted)
    .mark_line(point=True)
    .encode(
        x=alt.X("muestras", title="Muestras"),
        y=alt.Y("voltaje", scale=alt.Scale(domain=[0, 1]), title="Voltaje"),
    )
    .properties(width=700, height=400)
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

st.title("Gráfico de Irradiancia")
chart_2 = (
    alt.Chart(df_sorted)
    .mark_line(point=True)
    .encode(
        x=alt.X("muestras", title="Muestras"),
        y=alt.Y("irradiancia", scale=alt.Scale(domain=[-200, 2400]), title="Irradiancia"),
    )
    .properties(width=700, height=400)
    .interactive()
)

st.altair_chart(chart_2, use_container_width=True)

# Esperar antes de actualizar
time.sleep(1)
st.rerun()
