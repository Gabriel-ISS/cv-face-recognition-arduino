# Reconocimiento facial con Python y comunicación con Arduino

## Configuración inicial

Instala conda y luego ejecuta los siguientes comandos

```pwsh
# Crear el entorno. Usamos python 3.9 porque es compatible con la version de tensorflow que necesitamos
conda env create -f environment.yml

# activar el entorno
conda activate face-recognition-gpu

# Habilita las rutas largas para tensorflow en modo administrador
New-ItemProperty -Path"HKLM:\SYSTEM\CurrentControlSet\Control\FieSystem" -Name "LongPathsEnabled" -Value 1-PropertyType DWORD -Force
```

## Arranque

1. Compila el código del Arduino y cárgalo. Asegúrate de conectar cada servomotor en el sitio correcto.
1. Verifica el puerto COM en el que esta conectado el Arduino.
1. Agrega el archivo `server/config.py` y agrégale el siguiente contenido:
    ```python
    # debe coincidir con el puerto del Arduino
    COM_PORT = 6
    BAUD_RATE = 9600
    CAPTURE_WIDTH = 1920
    CAPTURE_HEIGHT = 1080
    TARGET_FPS = 60
    CAMERA = 0
    ```
1. Cierra Arduino IDE y cualquier otro programa que pueda esta utilizando el puerto.
1. Ejecuta `python -m server.main` para iniciar el proyecto.