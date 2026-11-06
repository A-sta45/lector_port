import streamlit as st
import serial
import pandas as pd
import time
import altair as alt

# Parámetros de conversión
V_REF = 5  # Voltaje de referencia del ADC
SENSIBILIDAD_SENSOR = 0.1  # Ajusta según tu sensor

# Funciones de conversión
def adc_to_voltage(adc_value):
    return (adc_value / 65535) * V_REF

def voltage_to_irradiance(voltage):
    return (voltage * 2400) - 200

# Inicialización de datos en session_state
if 'voltajes' not in st.session_state:
    st.session_state['voltajes'] = []
if 'irradiancias' not in st.session_state:
    st.session_state['irradiancias'] = []
if 'tiempos' not in st.session_state:
    st.session_state['tiempos'] = []
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()

st.title("Monitor de Voltaje e Irradiancia (Tiempo Real)")

# Leer dato serial
try:
    with serial.Serial('COM4', baudrate=115200, timeout=1) as ser:
        line = ser.readline().decode('utf-8').strip()
        if line:
            adc_value = int(line)
            voltaje = adc_to_voltage(adc_value)
            irradiancia = voltage_to_irradiance(voltaje)
            t = time.time() - st.session_state['start_time']

            st.session_state['voltajes'].append(voltaje)
            st.session_state['irradiancias'].append(irradiancia)
            st.session_state['tiempos'].append(t)

except Exception as e:
    st.write(f"Error: {e}")

# Calcular estadísticas
if st.session_state['voltajes']:
    df_metrics = pd.DataFrame({
        'Voltaje': st.session_state['voltajes'],
        'Irradiancia': st.session_state['irradiancias']
    })
    
    # Estadísticas para voltaje
    voltaje_promedio = df_metrics['Voltaje'].mean()
    voltaje_minimo = df_metrics['Voltaje'].min()
    voltaje_maximo = df_metrics['Voltaje'].max()
    voltaje_ultimo = df_metrics['Voltaje'].iloc[-1]
    
    # Estadísticas para irradiancia
    irradiancia_promedio = df_metrics['Irradiancia'].mean()
    irradiancia_minimo = df_metrics['Irradiancia'].min()
    irradiancia_maximo = df_metrics['Irradiancia'].max()
    irradiancia_ultimo = df_metrics['Irradiancia'].iloc[-1]

    # Mostrar métricas en columnas
    st.header("Métricas en Tiempo Real")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Voltaje (V)")
        st.metric("Promedio", f"{voltaje_promedio:.2f}")
        st.metric("Mínimo", f"{voltaje_minimo:.2f}")
        st.metric("Máximo", f"{voltaje_maximo:.2f}")
        st.metric("Último valor", f"{voltaje_ultimo:.2f}")
    
    with col2:
        st.subheader("Irradiancia (μW/cm²)")
        st.metric("Promedio", f"{irradiancia_promedio:.2f}")
        st.metric("Mínimo", f"{irradiancia_minimo:.2f}")
        st.metric("Máximo", f"{irradiancia_maximo:.2f}")
        st.metric("Último valor", f"{irradiancia_ultimo:.2f}")

    # Crear DataFrames para gráficos
    df_muestras = pd.DataFrame({
        'Muestra': range(1, len(df_metrics) + 1),
        'Voltaje': df_metrics['Voltaje'],
        'Irradiancia': df_metrics['Irradiancia']
    })
    
    df_tiempo = pd.DataFrame({
        'Tiempo': st.session_state['tiempos'],
        'Voltaje': df_metrics['Voltaje'],
        'Irradiancia': df_metrics['Irradiancia']
    })

    # Gráficos superiores (lado a lado)
    st.header("Visualización de Datos")
    col_top1, col_top2 = st.columns(2)
    
    with col_top1:
        st.subheader("Voltaje vs Muestras")
        chart = alt.Chart(df_muestras).mark_line().encode(
            x='Muestra',
            y=alt.Y('Voltaje', scale=alt.Scale(domain=[0, 5]))
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
    
    with col_top2:
        st.subheader("Irradiancia vs Muestras")
        chart = alt.Chart(df_muestras).mark_line().encode(
            x='Muestra',
            y=alt.Y('Irradiancia', scale=alt.Scale(domain=[-200, 10000]))
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

    # Gráficos inferiores (lado a lado)
    col_bottom1, col_bottom2 = st.columns(2)
    
    with col_bottom1:
        st.subheader("Voltaje vs Tiempo")
        st.line_chart(df_tiempo.set_index('Tiempo')['Voltaje'], height=300)
    
    with col_bottom2:
        st.subheader("Irradiancia vs Tiempo")
        st.line_chart(df_tiempo.set_index('Tiempo')['Irradiancia'], height=300)

# Actualización automática
time.sleep(1)
st.rerun()
