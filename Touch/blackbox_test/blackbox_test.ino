#include <TouchScreen.h>

// Define the pins for the 4-wire resistive touch screen
#define YP A0  // Y+ (Top)
#define XM A1  // X- (Left)
#define XP 7   // X+ (Right)
#define YM 6   // Y- (Bottom)

/*
// Define the touchscreen calibration values
#define TS_LEFT 150
#define TS_RT 920
#define TS_TOP 120
#define TS_BOT 940
*/

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Read the touch screen data
  TSPoint p = ts.getPoint();

  if (p.z > 15){
  // Print the touch screen data
    Serial.print("X = ");
    Serial.print(p.x);
    Serial.print("\tY = ");
    Serial.print(p.y);
    Serial.print("\tPressure = ");
    Serial.println(p.z);
  }

/*
  // Map the touch screen coordinates to the screen resolution
  int x = map(p.x, TS_LEFT, TS_RT, 0, 320); // adjust the screen resolution as needed
  int y = map(p.y, TS_TOP, TS_BOT, 0, 240); // adjust the screen resolution as needed

  // Print the mapped coordinates
  Serial.print("Mapped X = ");
  Serial.print(x);
  Serial.print("\tMapped Y = ");
  Serial.println(y);

  delay(50);
  */
}