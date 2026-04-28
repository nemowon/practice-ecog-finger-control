#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

// 你可以按自己的接线修改引脚
const int SERVO1_PIN = 3;
const int SERVO2_PIN = 5;
const int SERVO3_PIN = 7;
const int SERVO4_PIN = 9;

// 两个目标角度
const int ANGLE_A = 10;
const int ANGLE_B = 150;

void setup() {
  Serial.begin(9600);

  servo1.attach(SERVO1_PIN);
  servo2.attach(SERVO2_PIN);
  servo3.attach(SERVO3_PIN);
  servo4.attach(SERVO4_PIN);

  // 初始位置都设为 10°
  servo1.write(ANGLE_A);
  servo2.write(ANGLE_A);
  servo3.write(ANGLE_A);
  servo4.write(ANGLE_A);

  delay(1000);
  Serial.println("Arduino ready.");
  Serial.println("1/q -> Servo1: 10 / 90");
  Serial.println("2/w -> Servo2: 10 / 90");
  Serial.println("3/e -> Servo3: 10 / 90");
  Serial.println("4/r -> Servo4: 10 / 90");
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();

    switch (cmd) {
      case '1':
        servo1.write(ANGLE_A);
        Serial.println("Servo1 -> 10");
        break;

      case 'q':
        servo1.write(ANGLE_B);
        Serial.println("Servo1 -> 90");
        break;

      case 'w':
        servo2.write(ANGLE_A);
        Serial.println("Servo2 -> 10");
        break;

      case '2':
        servo2.write(ANGLE_B);
        Serial.println("Servo2 -> 90");
        break;

      case '3':
        servo3.write(ANGLE_A);
        Serial.println("Servo3 -> 10");
        break;

      case 'e':
        servo3.write(ANGLE_B);
        Serial.println("Servo3 -> 90");
        break;

      case '4':
        servo4.write(ANGLE_A);
        Serial.println("Servo4 -> 10");
        break;

      case 'r':
        servo4.write(ANGLE_B);
        Serial.println("Servo4 -> 90");
        break;

      default:
        // 忽略其他字符，比如换行
        break;
    }
  }
}