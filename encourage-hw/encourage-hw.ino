void setup() {
Serial.begin(9600); // set the baud rate
Serial.println("Ready"); // print "Ready" once
pinMode(2, OUTPUT);
}
void loop() {
  char inByte = ' ';
  if(Serial.available()){
    inByte = Serial.read();
    if(inByte == 33){
      digitalWrite(2, HIGH);
      Serial.println("HIGH");
    } else{
      digitalWrite(2, LOW);
      Serial.println("LOW");
    }
    
    delay(100);
  } else {
    digitalWrite(2, HIGH);
  }
}
