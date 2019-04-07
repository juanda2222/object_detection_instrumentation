#define signal A0
int flag = 0;                                     
void setup(){
    Serial.begin(9600);
    //unsigned long time1=0;
    //unsigned long time=0;      
    //time1=micros();
    //datos_B();
    datos_config();    
    //time=micros()-time1;
    //Serial.print(" Tiempo1: ");
    //Serial.println(time);
    //get_frecuencia_muestreo();
}

void loop(){  
    //unsigned long time1=0;
    //unsigned long time=0;      
    //time1=micros();
    delay(100);
    vector_datos();
    //time=micros()-time1;
    //Serial.print(" Tiempo2: ");
    //Serial.println(time);
}

void vector_datos(){
    
    int TxW = 87; // 0x57
	int TxX = 88; // 0x58
	int TxY = 89; // 0x59
	int TxZ = 90; // 0x5A
    int N = 185;
    int head = 1500;
    int datos[4*N+23];
    int Gain = 1;
    int i = 0;
    int count = 0;
    
    //DATOS DE T1R1
    datos[0] = head;
    datos[1] = TxW;
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
    datos[N+7] = TxX;
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
    datos[2*N+13] = TxY;
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
    datos[3*N+19] = TxZ;
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
void datos_config(){
    int head = 1;
    int sample = 8928;
    int resolution = 1023;
    int Vref = 5;
    int CR = 1;
    int datos_conf[5];
    int i = 0;
    datos_conf[0] = head;
    datos_conf[1] = sample;
    datos_conf[2] = resolution;
    datos_conf[3] = Vref;
    datos_conf[4] = CR;
    while(i <= 4){
        Serial.println(datos_conf[i]);
        i++;
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


