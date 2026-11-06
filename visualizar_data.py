import streamlit as st
import time
import altair as alt

# Inicializa la conexión usando st.connection
conn = st.connection("mysql", type="sql")



# Consulta los últimos
df = conn.query(
    "SELECT id, voltaje, irradiancia FROM muestras ORDER BY id DESC LIMIT 10;", ttl=0
)

# Reverse the order to plot correctly
df_sorted = df.iloc[::-1].sort_values(by="id")

# Ordenar los datos por id en orden ascendente para graficar correctamente
df_sorted = df.sort_values(by="id")

# Crear una nueva columna para representar el índice como "Cantidad de Datos"
df_sorted["muestras"] = range(1, len(df_sorted) + 1)

st.title("Tabla de Muestras")
# Mostrar tabla de datos
st.dataframe(df_sorted)


st.title("Gráfico de Voltaje")
# Graficar los últimos datos agregados
chart = (
    alt.Chart(df_sorted)
    .mark_line(point=True)
    .encode(
        x=alt.X("muestras", title="Muestras"),
        y=alt.Y("voltaje", scale=alt.Scale(domain=[0, 5]), title="Voltaje"),
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
        y=alt.Y("irradiancia", scale=alt.Scale(domain=[-200, 10000]), title="Irradiancia"),
    )
    .properties(width=700, height=400)
    .interactive()
)

st.altair_chart(chart_2, use_container_width=True)

# Esperar antes de actualizar
time.sleep(1)
st.rerun()