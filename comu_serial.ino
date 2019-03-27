#define signal A0
                                        
void setup(){
    Serial.begin(9600);
    //get_frecuencia_muestreo();
}

void loop(){

    datos_serial();
    delay(100);
     
}
void datos_serial(){
    //DATOS DE T1R1
    int head = 88;
    int N = 200;
    int Gain = 1023;
    int i = 0;
    int count = 0;
    Serial.println(head);
    Serial.println(0);
    Serial.println(Gain);
    Serial.println(N);
    while(count <= N){
        Serial.println(analogRead(signal));
        count++;
    }
    Serial.println(1);
    //DATOS DE T1R2
    Serial.println(head);
    Serial.println(1);
    Serial.println(Gain);
    Serial.println(N);
    count = 0;
    while(count <= N){
        Serial.println(analogRead(signal));
        count++;
    }
    Serial.println(1);
    //DATOS DE T2R1
    Serial.println(head);
    Serial.println(2);
    Serial.println(Gain);
    Serial.println(N);
    count = 0;
    while(count <= N){
        Serial.println(analogRead(signal));
        count++;
    }
    Serial.println(1);
    //DATOS DE T2R2
    Serial.println(head);
    Serial.println(2);
    Serial.println(Gain);
    Serial.println(N);
    count = 0;
    while(count <= N){
        Serial.println(analogRead(signal));
        count++;
    }
    Serial.println(1);   
}

void get_frecuencia_muestreo(){

  unsigned long time1=0;
  unsigned long time=0;
  Serial.println("*************************");
  Serial.println("ENSAYO TIEMPO DE MUESTRO:");
  Serial.println("*************************");
  for(byte i =0; i<4; i++){
    time1=micros();
    int A=analogRead(A0);
    time=micros()-time1;
    Serial.print(" Muestra: ");
    Serial.print(i+1);
    Serial.print(" Tiempo: ");
    Serial.println(time);
  }

}

