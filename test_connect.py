import mysql.connector

def get_connection():
    print('Se va a conectar')
    return mysql.connector.connect(
        host='127.0.0.1',
        # host='localhost',
        # host='192.168.1.117',
        user='root',      # Cambia por tu usuario de MySQL
        password='', # Cambia por tu contraseña de MySQL
        database='proyecto_piranometro',
        port=3306
    )

def insertar_datos(tiempo, voltaje, irradiancia):
    conn = get_connection()
    print('Se crea la conexion')
    cursor = conn.cursor()
    print('SE crea el cursor')
    try:
        # Insertar en la tabla de voltaje
        cursor.execute("INSERT INTO voltaje (tiempo, voltaje) VALUES (%s, %s)", (tiempo, voltaje))
        # Insertar en la tabla de irradiancia
        cursor.execute("INSERT INTO irradiancia (tiempo, irradiancia) VALUES (%s, %s)", (tiempo, irradiancia))
        conn.commit()
        print('Se guarda la informacion')
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")
    finally:
        cursor.close()
        conn.close()


insertar_datos(3,3,3)