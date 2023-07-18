// Pins
int DMDpinOUT = 13;
int DMDpinIN = 12;

int PDvaluepin = A0;

// Values
float PDvalue;


void setup() {
  Serial.begin(115200); // max baud rate for UNO
  pinMode(DMDpinOUT, OUTPUT);  // sets the digital pin 13 as output
  pinMode(DMDpinIN, INPUT);    // sets the digital pin 12 as input
}

void loop() {
  int DMDout = digitalRead(DMDpinOUT);
  if(DMDout == HIGH){
    PDvalue = analogRead(PDvaluepin);
    Serial.println(PDvalue); // convert this later to some meaningful value
    
    digitalWrite(DMDpinIN, HIGH);
    delay(50); // I don;t know how long should be the triggering pulse
    digitalWrite(DMDpinIN, LOW);
  }
}
