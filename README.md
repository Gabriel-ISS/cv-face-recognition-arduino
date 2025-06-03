# Reconocimiento facial con Python y comunicación con Arduino

## Configuración inicial

⚠️ IMPORTANTE: La dependencia `mediapipe` no esta disponible en Python 3.13. Usa la version 3.12.

```bash
# crear el entorno
python -m venv .venv

# activar el entorno
.venv\Scripts\activate

# instalar las librerias necesarias
pip install -r requirements.txt
```

## Arranque

1. Compila el código del Arduino y cárgalo. Asegúrate de conectar cada servomotor en el sitio correcto.
1. Verifica el puerto COM en el que esta conectado el Arduino.
1. Agrega el archivo `vision_python/config.py` y agrégale el siguiente contenido:
    ```python
    # debe coincidir con el puerto del Arduino
    COM_PORT = 6
    BAUD_RATE = 9600
    ```
1. Cierra Arduino IDE y cualquier otro programa que pueda esta utilizando el puerto.
1. Ejecuta `python vision_python/main.py` para iniciar el proyecto.