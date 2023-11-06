// Código de ativação das solenides Arduino

// Bibliotecas
import serial

// Declaração de variáveis globais
Serial.setTimeout(1);

// Configurações do Arduino
void setup() {
  Serial.begin(115200);

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  while (!Serial.available());
  x = Serial.readString();
}