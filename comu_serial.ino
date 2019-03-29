#define signal A0
int flag = 0;                                     
void setup(){
    Serial.begin(9600);
    datos_config();    
    //get_frecuencia_muestreo();
}

void loop(){        
    delay(100);
    vector_datos();
}

void vector_datos(){
    int N = 200;
    int head = 1500;
    int datos[4*N+23];
    int Gain = 1023;
    int i = 0;
    int count = 0;
    //DATOS DE T1R1
    datos[0] = head;
    datos[1] = 0;
    datos[2] = Gain;
    datos[3] = N;
    count = 0;
    while(count <= N){
        datos[count+4] = analogRead(signal);
        count++;
    }
    datos[N+5] = 1;
    //DATOS DE T1R2
    datos[N+6] = head;
    datos[N+7] = 1;
    datos[N+8] = Gain;
    datos[N+9] = N;
    count = 0;
    while(count <= N){
        datos[N+count+10] = analogRead(signal);
        count++;
    }
    datos[2*N+11] = 1;
    //DATOS DE T2R1
    datos[2*N+12] = head;
    datos[2*N+13] = 2;
    datos[2*N+14] = Gain;
    datos[2*N+15] = N;
    count = 0;
    while(count <= N){
        datos[2*N+count+16] = analogRead(signal);
        count++;
    }
    datos[3*N+17] = 1;
    //DATOS DE T2R2
    datos[3*N+18] = head;
    datos[3*N+19] = 3;
    datos[3*N+20] = Gain;
    datos[3*N+21] = N;
    count = 0;
    while(count <= N){
        datos[3*N+count+22] = analogRead(signal);
        count++;
    }
    datos[4*N+23] = 1;
    //ENVIO DATOS
    count = 0;
    while(count <= 4*N+23){
        Serial.println(datos[count]);
        count++;
    }
    
    
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

