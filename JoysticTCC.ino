/*
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Leitura e mapeamento das posições do joystick
*/
int DefValueY, sensorValueY;
int DefValueX, sensorValueX;

void setup() {
  Serial.begin(9600);
  DefValueY = 512-analogRead(1);
  DefValueX = 512-analogRead(0);
  delay(10);
  
}

void loop() {
  

  sensorValueY = 512-analogRead(1)-DefValueY;
  sensorValueX = 512-analogRead(0)-DefValueX;

  if ((sensorValueY>255)&&(sensorValueX<20)) {
    delay(1000); //Simulando o tempo de transmissão dos dados do capacete
    Serial.println("frente");
  }else if ((sensorValueY<-255)&&(sensorValueX<20)) {
    delay(1000);
    Serial.println("tras");
  }else if ((sensorValueY<20)&&(sensorValueX>255)) {
    delay(1000);
    Serial.println("direita");
  }else if ((sensorValueY<20)&&(sensorValueX<-255)) {
    delay(1000);
    Serial.println("esquerda");
  }else if ((sensorValueY<20)&&(sensorValueY>-20)&&(sensorValueX>-20)&&(sensorValueX<20)) {
    delay(1000);
    Serial.println("parar");

}
}
