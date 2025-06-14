#include <max6675.h>

// Define pins for Sensor 1
int soPin1 = 19;
int sckPin1 = 18;
int csPin1 = 5;

// Define pins for Sensor 2
int soPin2 = 21;
int sckPin2 = 18; // You can share the SCK pin
int csPin2 = 4;

// Initialize the MAX6675 objects
MAX6675 thermocouple1(sckPin1, csPin1, soPin1);
MAX6675 thermocouple2(sckPin2, csPin2, soPin2);

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("MAX6675 Dual Sensor Test");
}

void loop() {
  double temp1 = thermocouple1.readCelsius();
  double temp2 = thermocouple2.readCelsius();
  
  // Send data to serial in CSV format
  Serial.print(temp1);
  Serial.print(",");
  Serial.println(temp2);
  
  delay(1000); // 1-second delay
}