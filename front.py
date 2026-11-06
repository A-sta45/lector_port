import streamlit as st
import serial
import pandas as pd
import time

# Parámetros de conversión
V_REF = 5  # Voltaje de referencia del ADC
SENSIBILIDAD_SENSOR = 0.1  # Ajusta según tu sensor (ejemplo: 0.1 μW/(cm²·mV))

# Funciones de conversión
def adc_to_voltage(adc_value):
    return (adc_value / 65535) * V_REF

def voltage_to_irradiance(voltage):
    return (voltage * 2400) - 200   # Ajusta según tu sensor

# Inicialización de listas en session_state
if 'voltajes' not in st.session_state:
    st.session_state['voltajes'] = []
if 'irradiancias' not in st.session_state:
    st.session_state['irradiancias'] = []
if 'tiempos' not in st.session_state:
    st.session_state['tiempos'] = []
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()

st.title("Monitor de Voltaje e Irradiancia (actualización en tiempo real)")

# Leer dato serial cada vez que se recarga la app
try:
    with serial.Serial('COM4', baudrate=115200, timeout=1) as ser:
        line = ser.readline().decode('utf-8').strip()
        adc_value = int(line)
        voltaje = adc_to_voltage(adc_value)
        irradiancia = voltage_to_irradiance(voltaje)
        t = time.time() - st.session_state['start_time']

        st.session_state['voltajes'].append(voltaje)
        st.session_state['irradiancias'].append(irradiancia)
        st.session_state['tiempos'].append(t)

        # Mostrar el último dato recibido y sus conversiones
        st.metric("Último valor ADC", adc_value)
        st.metric("Último voltaje (V)", f"{voltaje:.3f}")
        st.metric("Última irradiancia (μW/cm²)", f"{irradiancia:.3f}")

except Exception as e:
    st.write(f"Error al leer/conversión: {e}")

# Crear DataFrames para graficar
df_voltaje = pd.DataFrame({
    'Tiempo': st.session_state['tiempos'],
    'Voltaje': st.session_state['voltajes']
})
df_irradiancia = pd.DataFrame({
    'Tiempo': st.session_state['tiempos'],
    'Irradiancia': st.session_state['irradiancias']
})

# Graficar una debajo de la otra
st.subheader("Voltaje vs Tiempo")
st.line_chart(df_voltaje.set_index('Tiempo'))

st.subheader("Irradiancia vs Tiempo")
st.line_chart(df_irradiancia.set_index('Tiempo'))

# Espera 1 segundo antes de recargar
time.sleep(1)
st.rerun()
