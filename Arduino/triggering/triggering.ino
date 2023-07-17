// Pins
int DMDpinOUT = 13;
int DMDpinIN = 12;

int PDvaluepin = A0;

// Values
typedef union {
  float floatingPoint;
  byte binary[8];
} binaryFloat;

binaryFloat PDvalue;


void setup() {
  Serial.begin(115200); // max baud rate for UNO
  pinMode(DMDpinOUT, OUTPUT);  // sets the digital pin 13 as output
  pinMode(DMDpinIN, INPUT);    // sets the digital pin 7 as input
}

void loop() {
  int DMDout = digitalRead(DMDpinOUT);
  Serial.println(DMDout);
  if(DMDout == 1){
    Serial.print("PD value: ");
    PDvalue.floatingPoint = analogRead(PDvaluepin);
    Serial.println(PDvalue.floatingPoint);
    Serial.write(PDvalue.binary, 8);
    digitalWrite(DMDpinIN, 1);
  }
}
