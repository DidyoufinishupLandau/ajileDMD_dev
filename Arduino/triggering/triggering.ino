// Pins
int FROM_DMD_OUT_pin = 13; // connected to DMD output
int TO_DMD_IN_pin = 12; // connected to DMD input

int PDvalue_pin = A0;

// Values
int PDvalue;
int DMDout;


void setup() {
  Serial.begin(9600); // max baud rate for UNO
  pinMode(FROM_DMD_OUT_pin, INPUT);  // sets the digital pin 13 as arduino input
  pinMode(TO_DMD_IN_pin, OUTPUT);    // sets the digital pin 12 as arduino output
  DMDout = LOW;
}

void loop() {
  /*
  // Test for PD
  PDvalue = analogRead(PDvalue_pin);
  Serial.println(PDvalue); // convert this later to some meaningful value
  */
  // Test for DMD
  // **** For testing - I must see change in sequence every 0.5s
    /*
  DMDout = digitalRead(FROM_DMD_OUT_pin); // trigger timeframe is 1/16 ms

  if(DMDout == HIGH){
    Serial.println(analogRead(PDvalue_pin)); // convert this later to some meaningful value
  }*/
    digitalWrite(TO_DMD_IN_pin, HIGH);
    delay(1); // I don;t know how long should be the triggering pulse
    digitalWrite(TO_DMD_IN_pin, LOW);
    delay(1000);
  //
  /*if(DMDout == HIGH){
    PDvalue = analogRead(PDvalue_pin);
    Serial.println(PDvalue); // convert this later to some meaningful value
    
  }*/
  //DMDout = digitalRead(FROM_DMD_OUT_pin);

  /*
  // Actuall code
  if(DMDout == HIGH){
    PDvalue = analogRead(PDvaluepin);
    Serial.println(PDvalue); // convert this later to some meaningful value
    
    digitalWrite(TO_DMD_IN_pin, HIGH);
    delay(250); // I don;t know how long should be the triggering pulse
    digitalWrite(TO_DMD_IN_pin, LOW);
  }
  DMDout = digitalRead(FROM_DMD_OUT_pin);
  */
}
