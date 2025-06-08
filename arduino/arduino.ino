#include <Servo.h>
Servo servoH;                   // Servo encargado del movimineto horizontal
Servo servoV;                   // Servo encargado del movimineto vertical
String entradaSerial = "";      // String para almacenar entrada
bool entradaCompleta = false;   // Indicar si el String está completo
int velocidadDeConexion = 9600; // Establecemos a cuantos baudios debe ir la conexion

// pines de conexión PWM al servo
int pServoH = 9;
int pServoV = 10;
int pulsoMinimo = 580;  // Duración en microsegundos del pulso para girar 0º
int pulsoMaximo = 2500; // Duración en microsegundos del pulso para girar 180º
int angulo = 0;         // Variable para guardar el angulo que deseamos de giro

void setup()
{
  // configuramos los servos
  servoH.attach(pServoH, pulsoMinimo, pulsoMaximo);
  servoV.attach(pServoV);

  // establecemos un angulo inicial
  servoH.write(0);
  servoV.write(15);

  // configuramos la conexion serial
  Serial.begin(velocidadDeConexion);
}

void loop()
{
  // si los datos no se terminaron de enviar cancelamos la ejecucion de la iteracion del bucle
  if (!entradaCompleta)
    return;

  // movemos el servo en horizontal
  if (entradaSerial == "izq1")
  {
    moverServo("x", -15);
  }
  else if (entradaSerial == "izq2")
  {
    moverServo("x", -5);
  }
  else if (entradaSerial == "izq3")
  {
    moverServo("x", 5);
  }
  else if (entradaSerial == "ctr")
  {
    moverServo("x", 15);
  }
  else if (entradaSerial == "der3")
  {
    moverServo("x", 25);
  }
  else if (entradaSerial == "der2")
  {
    moverServo("x", 35);
  }
  else if (entradaSerial == "der1")
  {
    moverServo("x", 45);
  }
  else if (entradaSerial == "arriba")
  {
    moverServo("y", 30);
  }
  else if (entradaSerial == "abajo")
  {
    moverServo("y", 0);
  }
  else
  {
    // Si el comando no es valido enviamos un error
    Serial.println("Error: El dato recibido es inválido!!\n");
  }

  // nos aseguramos de reestablecer los datos necesarios
  entradaSerial = "";
  entradaCompleta = false;
}

// Función que se activa cuando ocurre cualquier evento relacionado a la conexion serial
// como al recibir algo por el puerto o al interrumpir la conexion.
void serialEvent()
{

  // mientras la conexion serial se mantenga abierta y no se haya terminado la entrada...
  while (Serial.available() && !entradaCompleta)
  {

    // Obtener bytes de entrada y lo convertimos en un caracter
    char inChar = (char)Serial.read();

    // Para saber si el string está completo, se detendrá al recibir
    // el caracter de salto de línea \n
    if (inChar == '\n')
    {
      entradaCompleta = true;
    }
    else
    {
      // si el caracter no es \n --> agregar al String de entrada
      entradaSerial += inChar;
    }
  }
}

void moverServo(String eje, int angulo)
{
  // obtenemos el angulo como adena de texto
  String anguloStr = (String)angulo;

  // Enviamos el mensaje con un salto de linea
  Serial.println("Movemos " + anguloStr + " en el eje " + eje);

  // Movemos el servo
  if (eje == "x")
  {
    servoH.write(angulo);
  }
  else if (eje == "y")
  {
    servoV.write(angulo);
  }
  else
  {
    // esto no deberia pasar
  }
}
