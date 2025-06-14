from typing import Union
import serial


class ConnectionBridge:
    """Utilidad para administrar la comunicación con el Arduino. Actualmente utiliza una conexión serial.

    Comunicación serial: facilita el envío y recepción de datos en forma de señales eléctricas a través de cables,
    lo que es útil en aplicaciones donde se requiere una comunicación simple y directa. Se le dice serial porque
    los datos se envían de un bit a la vez, en una secuencia continua.
    """

    cached_commands = {}

    ser: Union[serial.Serial, None] = None
    debug: bool = False

    def __init__(self, COM: int, BAUD: int, debug: bool = False):
        self.debug = debug
        if not debug:
            self.ser = serial.Serial("COM" + str(COM), BAUD)

    def enviar(self, comando: str, cache_key: str = ""):
        """Envía un comando

        Args:
            comando (str): Comando a enviar.
            cache_key (str, optional): Evita que el mismo comando se envié de seguido. Por defecto es "".
        """
        if comando == self.cached_commands.get(cache_key, ""):
            return

        print(f"Enviando: {comando}")

        if self.ser:
            self.ser.write((comando + "\n").encode())

        if cache_key:
            self.cached_commands[cache_key] = comando

    def cerrar(self):
        if self.ser is not None:
            self.ser.close()
            self.cached_commands.clear()
