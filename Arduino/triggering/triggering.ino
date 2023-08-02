// Pins
int FROM_DMD_OUT_pin = 13; // connected to DMD output
int TO_DMD_IN_pin = 12; // connected to DMD input

int PDvalue_pin = A0;

// Values
int PDvalue;
int DMDout;
const float ADC_to_V = 5.0/1023; // Volts 


void setup() {
  Serial.begin(115200); // 115200 max baud rate for UNO
  pinMode(FROM_DMD_OUT_pin, INPUT);  // sets the digital pin 13 as arduino input
  pinMode(TO_DMD_IN_pin, OUTPUT);    // sets the digital pin 12 as arduino output
  DMDout = LOW;
}

void acq(){
  while(true){   
    digitalWrite(TO_DMD_IN_pin, HIGH);
    //delay(1/32); // I don;t know how long should be the triggering pulse - apparently it's not needed. Arduino is slow enought with switching the state so DMD can detect this trigger
    digitalWrite(TO_DMD_IN_pin, LOW); 
    delay(1/256);
    DMDout = digitalRead(FROM_DMD_OUT_pin);
    if(DMDout == HIGH){
    PDvalue = analogRead(PDvalue_pin);
    Serial.println(PDvalue); // convert this later to some meaningful value
    
  }
  }
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
  //delay(1/32); // I don;t know how long should be the triggering pulse - apparently it's not needed. Arduino is slow enought with switching the state so DMD can detect this trigger
  digitalWrite(TO_DMD_IN_pin, LOW); 
  delay(1/256);
  DMDout = digitalRead(FROM_DMD_OUT_pin);
  if(DMDout == HIGH){
    PDvalue = analogRead(PDvalue_pin);
    Serial.println(PDvalue); // convert this later to some meaningful value
    
  }
  /*
  // Actuall code
  if(DMDout == HIGH){
    PDvalue = analogRead(PDvalue_pin);
    Serial.println(PDvalue); // convert this later to some meaningful value
    
    digitalWrite(TO_DMD_IN_pin, HIGH);
    digitalWrite(TO_DMD_IN_pin, LOW);
  }
  DMDout = digitalRead(FROM_DMD_OUT_pin);
  */
}
