#include <TouchScreen.h>

// Defina os pinos corretos para a tela de toque
#define XP A0
#define XM A1
#define YP A2
#define YM A3

TouchScreen ts = TouchScreen(XP, YP, XM, YM);

void setup() {
    Serial.begin(9600);
}

void loop() {
    TSPoint p = ts.getPoint();

    if (p.z > 25){
      Serial.print("x=");
      Serial.print(p.x);
      Serial.print(" | y=");
      Serial.print(p.y);
      Serial.print(" | z=");
      Serial.println(p.z);
    }
    /*
    if (p.z > 10) { // Se o toque for detectado
        int16_t x = map(p.x, 0, 138, 0, 320); // Mapeie para a largura da tela
        int16_t y = map(p.y, 0, 65, 0, 240); // Mapeie para a altura da tela
        Serial.print("Coordenadas: X=");
        Serial.print(x);
        Serial.print(", Y=");
        Serial.println(y);
    }*/
}
