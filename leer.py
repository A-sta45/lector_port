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
                print (data) 
            except Exception as e:
                print(f"Error procesando datos: {e}")

except KeyboardInterrupt:
    print("\nLectura interrumpida por el usuario.")
finally:
    ser.close()
    print("Puerto cerrado.")
