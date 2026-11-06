import serial

def convertir_a_voltaje(valor_adc):
    """Convierte el valor ADC (0-65535) a voltaje (0-3.3V)"""
    try:
        valor = float(valor_adc)
        return valor * 3.3 / 65535
    except ValueError:
        return None

ser = serial.Serial(
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

print(f"Puerto abierto: {ser.name}")

try:
    while True:
        data = ser.readline()
        if data:
            try:
                # Decodificar y limpiar datos
                decoded_data = data.decode('utf-8', errors='ignore').strip()
                
                # Extraer valor numérico (admite formatos como "ADC:12345" o "0.75V")
                if decoded_data:
                    # Caso 1: Si viene como valor crudo (ej: "21567")
                    if decoded_data.isdigit():
                        voltaje = convertir_a_voltaje(decoded_data)
                        print(f"Voltaje: {voltaje:.2f}V" if voltaje is not None else "Formato inválido")
                    
                    # Caso 2: Si viene en formato "ADC:valor" (como en los ejemplos anteriores)
                    elif "ADC:" in decoded_data:
                        adc_value = decoded_data.split(':')[-1].strip()
                        voltaje = convertir_a_voltaje(adc_value)
                        print(f"Voltaje: {voltaje:.2f}V" if voltaje is not None else "Formato ADC inválido")
                    
                    # Caso 3: Si ya viene como voltaje (ej: "1.23V")
                    elif 'V' in decoded_data:
                        print(f"Dato recibido: {decoded_data}")
                    
                    else:
                        print(f"Dato crudo: {decoded_data}")

            except Exception as e:
                print(f"Error procesando datos: {e}")

except KeyboardInterrupt:
    print("\nLectura interrumpida por el usuario.")
finally:
    ser.close()
    print("Puerto cerrado.")
