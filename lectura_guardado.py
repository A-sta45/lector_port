import serial
import mysql.connector
import time

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',         # Cambia por tu usuario
    'password': '',    # Cambia por tu contraseña
    'database': 'proyecto_piranometro',
    'port': 3306
}

# Parámetros de conversión
V_REF = 3.3
#3.3

def adc_to_voltage(adc_value):
    return (adc_value / 65535) * V_REF

def voltage_to_irradiance(voltage):
    return (voltage * 2400) - 200

def insertar_datos( voltaje, irradiancia):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    #cursor.execute("INSERT INTO voltaje (tiempo, voltaje) VALUES (%s, %s)", (tiempo, voltaje))
    cursor.execute("INSERT INTO muestras (voltaje, irradiancia) VALUES (%s, %s)", (voltaje, irradiancia))
    conn.commit()
    cursor.close()
    conn.close()

start_time = time.time()

with serial.Serial('COM4', baudrate=115200, timeout=1) as ser:
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(line)
        if line:
            try:
                adc_value = int(line)
                voltaje = adc_to_voltage(adc_value)
                irradiancia = voltage_to_irradiance(voltaje)
                t = time.time() - start_time
                insertar_datos( voltaje, irradiancia)
                print(f"Guardado:  V={voltaje:.3f}, Irr={irradiancia:.3f}")
            except Exception as e:
                print(f"Error: {e}")
        