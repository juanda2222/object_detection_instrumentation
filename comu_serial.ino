#define signal A0
                                        
void setup(){
    Serial.begin(9600);
}

void loop(){
    int N = 1024;
    int Gain = 1024;
    int i = 0;
    int cadena_datos[N+5];
    cadena_datos[0] = 2;
    cadena_datos[1] = 0;
    cadena_datos[2] = Gain;
    cadena_datos[3] = N;
    while(i <= N+4)
    {
        cadena_datos[i+4] = analogRead(signal);
        i++;
    }
    cadena_datos[N+5] = 1;
    for(int a = 0; a <= N+5; a++)
    {
        Serial.println(cadena_datos[a]);       
    } 
     delay(100);
}