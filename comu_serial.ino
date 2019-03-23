#define signal A0
float  serial_arduino = 0;
                                        
void setup(){

    Serial.begin(9600);

}

void loop(){
    int N = 30;
    int Gain = 1024;
    int i = 0;
    float cadena_datos[N+5];
    cadena_datos[0] = 2;
    cadena_datos[1] = 0;
    cadena_datos[2] = Gain;
    cadena_datos[3] = N;
    cadena_datos[N+5] = 1;
    for( i = 0; i <= N+4; i++)
    {
       cadena_datos[i+4] = analogRead(signal);
    }
    
    for( i = 0; i <= N+5; i++)
    {
       Serial.println(cadena_datos[i]);
    }

    delay(100);

}