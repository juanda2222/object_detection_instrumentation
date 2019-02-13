#define signal A0
float  serial_arduino = 0;

void setup(){

    Serial.begin(9600);

}

void loop(){

    serial_arduino = analogRead(signal)*5.0/1024;
    Serial.println(serial_arduino);
    delay(100);

}