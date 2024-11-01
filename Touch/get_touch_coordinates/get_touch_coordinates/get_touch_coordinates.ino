#include <TouchScreen.h>

// Defina os pinos da tela touch
#define YP A1  // Y+ ao pino A1 (Preto)
#define XM A2  // X- ao pino A2 (Verde)
#define YM 7   // Y- ao pino digital 7 (Branco)
#define XP 6   // X+ ao pino digital 6 (Vermelho)

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

void setup() {
  Serial.begin(9600);
  Serial.println("Touch Screen Calibration");
}

void loop() {
  TSPoint p = ts.getPoint();
  // Configurar os pinos para entrada e saída de forma correta
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);

  if (p.z > ts.pressureThreshhold) {
    Serial.print("X = "); Serial.print(p.x);
    Serial.print("\tY = "); Serial.println(p.y);
  }
  delay(100);
}

/* OBSERVADO NO MONITOR SERIAL
MEIO DA TELA É 500, 500
FAIXA DE VALORES EM X: 100 ~ 800 da esquerda pra direita
FAIXA DE VALORES EM Y: 300 ~ 700 de cima pra baixo
*/