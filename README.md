# Lector de Puerto Serial

Herramientas en Python para leer datos de un sensor analógico a través de **puerto serial** (Arduino/microcontrolador), convertirlos a voltaje/irradiancia y visualizarlos en tiempo real.

## Contenido

- **`main.py`** / **`leer.py`** / **`prueba.py`** — lectura básica del puerto serial y conversión del valor ADC a voltaje.
- **`front.py`** / **`visualizar_data.py`** / **`visualizar_data2.py`** — interfaces con **Streamlit** que grafican en vivo el voltaje y la irradiancia calculada a partir de los datos del sensor.
- **`lectura_guardado.py`** — lee el puerto serial y guarda los datos en una base de datos **MySQL**.
- **`test_connect.py`** — prueba de conexión a MySQL.
- **`.streamlit/secrets.toml`** — configuración de conexión a MySQL usada por Streamlit (datos locales, sin contraseña real por defecto).

## Configuración

Antes de ejecutar, ajusta en el código:

- El puerto serial (`COM4` en Windows, o algo como `/dev/ttyUSB0` en Linux).
- Los datos de conexión a MySQL en `.streamlit/secrets.toml` si vas a usar `lectura_guardado.py` o las vistas de Streamlit con base de datos.

## Instalación y ejecución

```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Lectura simple por consola
python main.py

# Visualización en tiempo real
streamlit run front.py
```
