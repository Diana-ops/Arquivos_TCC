/*
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Recebe as mensagens transmitidas do raspberry para o acionamento do carrinho
*/
#include <ESP8266WiFi.h> // Importa a Biblioteca ESP8266WiFi
#include <PubSubClient.h> // Importa a Biblioteca PubSubClient
 
//defines:
//defines de id mqtt e tópicos para publicação e subscribe6
#define TOPICO_SUBSCRIBE "Sara"     //tópico MQTT de escuta. 
                                                 //ATENÇÃO: deve ser o mesmo tópico de publish utilizado na Raspberry PI!!!
                                                  
#define ID_MQTT  "Sara"     //id mqtt (para identificação de sessão)
                                        //IMPORTANTE: este deve ser único no broker (ou seja, 
                                        //            se um client MQTT tentar entrar com o mesmo 
                                        //            id de outro já conectado ao broker, o broker 
                                        //            irá fechar a conexão de um deles).
                                
 
//defines - mapeamento de pinos do NodeMCU
#define D0    16 
#define D1    5
#define D2    4
#define D3    0
#define D4    2
#define D5    14
#define D6    12
#define D7    13
#define D8    15
#define D9    3
#define D10   1 
 
// Conexão WIFI
const char* SSID = ""; // "__" / nome da rede WI-FI que deseja se conectar
const char* PASSWORD = ""; // "" Senha da rede WI-FI que deseja se conectar
  
// MQTT
const char* BROKER_MQTT = "diana-desktop.local"; //URL do broker MQTT que se deseja utilizar
int BROKER_PORT = 1883; // Porta do Broker MQTT
 
//Variáveis e objetos globais
WiFiClient espClient; // Cria o objeto espClient
PubSubClient MQTT(espClient); // Instancia o Cliente MQTT passando o objeto espClient
 
//variável que armazena o estado atual da saídai
char EstadoSaida1 = '0'; 
char EstadoSaida2 = '0';
char EstadoSaida3 = '0';
char EstadoSaida4 = '0';

char CmdNodeMCU1[4] = {"BT1"}; //Frente
char CmdNodeMCU2[4] = {"BT2"}; //Tras

char CmdNodeMCU3[4] = {"BT3"}; //Esquerda
char CmdNodeMCU6[4] = {"BT6"}; //Esquerda para Uso Manual 

char CmdNodeMCU4[4] = {"BT4"}; //Direita
char CmdNodeMCU7[4] = {"BT7"}; //Direita para Uso Manual 

char CmdNodeMCU5[4] = {"BT5"}; //Parar


/*Configurações do Carrinho*/
int motor1_frente = D0;
int motor1_tras = D1;
int motor2_frente = D2;
int motor2_tras = D3;

//ATENÇÃO: troque o "BBB" por um dos códigos enviados pela Raspberry PI ("BT1", "BT2", "BT3", "BT4" ou "BT5"),
                                       //         de modo que cada NodeMCU "espere" apenas por um deles
  
//Prototypes
void initSerial();
void initWiFi();
void initMQTT();
void reconectWiFi(); 
void mqtt_callback(char* topic, byte* payload, unsigned int length);
void VerificaConexoesWiFIEMQTT(void);
void InitOutput(void);
 
/* 
 *  Implementações das funções
 */
void setup() 
{
    //inicializações:
    InitOutput();
    initSerial();
    initWiFi();
    initMQTT();
}
  
//Função: inicializa comunicação serial com baudrate 115200 (para fins de monitorar no terminal serial 
//        o que está acontecendo.
//Parâmetros: nenhum
//Retorno: nenhum
void initSerial() 
{
    Serial.begin(115200);
}
 
//Função: inicializa e conecta-se na rede WI-FI desejada
//Parâmetros: nenhum
//Retorno: nenhum
void initWiFi() 
{
    delay(10);
    Serial.println("------Conexao WI-FI------");
    Serial.print("Conectando-se na rede: ");
    Serial.println(SSID);
    Serial.println("Aguarde");
     
    reconectWiFi();
}
  
//Função: inicializa parâmetros de conexão MQTT(endereço do 
//        broker, porta e seta função de callback)
//Parâmetros: nenhum
//Retorno: nenhum
void initMQTT() 
{
    //Serial.println("Iniciando conexão");
    MQTT.setServer(BROKER_MQTT, BROKER_PORT);   //informa qual broker e porta deve ser conectado
    MQTT.setCallback(mqtt_callback);            //atribui função de callback (função chamada quando qualquer informação de um dos tópicos subescritos chega)
}
  
//Função: função de callback 
//        esta função é chamada toda vez que uma informação de 
//        um dos tópicos subescritos chega)
//Parâmetros: nenhum
//Retorno: nenhum

void off()
{
   digitalWrite(motor1_frente,LOW);
   digitalWrite(motor2_frente,LOW);
   digitalWrite(motor1_tras,LOW);
   digitalWrite(motor2_tras,LOW);
}
void mqtt_callback(char* topic, byte* payload, unsigned int length) 
{
    char MsgRecebida[3];
     
    //se a mensagem não tem três caracteres (ou seja, não é "BT1", "BT2", "BT3", "BT4" ou "BT5"), 
    //automaticamente ela é inválida. Nesse caso, nada mais é feito com a mensagem recebida.
    if (length != 3)
      return;
 
    //obtem a string do payload recebido
    for(int i = 0; i < length; i++) 
       MsgRecebida[i] = (char)payload[i];
    
    //avalia se a mensagem é para este NodeMCU
    if (memcmp(MsgRecebida,CmdNodeMCU1,3) == 0) //Frente
    {
        digitalWrite(motor1_frente,HIGH);
        digitalWrite(motor2_frente,HIGH);
        digitalWrite(motor1_tras,LOW);
        digitalWrite(motor2_tras,LOW);
        Serial.println("Frente");
          
    }
    if (memcmp(MsgRecebida,CmdNodeMCU2,3) == 0) //Tras
    {

           digitalWrite(motor1_tras,HIGH);
           digitalWrite(motor2_tras,HIGH);
           digitalWrite(motor1_frente,LOW);
           digitalWrite(motor2_frente,LOW);
           Serial.println("Tras");
    }
    if (memcmp(MsgRecebida,CmdNodeMCU3,3) == 0) //Esquerda
    {

           digitalWrite(motor1_frente,LOW);
           digitalWrite(motor2_frente,HIGH);
           digitalWrite(motor1_tras,LOW);
           digitalWrite(motor2_tras,LOW);
           Serial.println("Esquerda");
       
    }
    if (memcmp(MsgRecebida,CmdNodeMCU6,3) == 0) //Esquerda para Uso Manual
    {

           digitalWrite(motor1_frente,LOW);
           digitalWrite(motor2_frente,HIGH);
           digitalWrite(motor1_tras,LOW);
           digitalWrite(motor2_tras,LOW);
           delay(500);
           digitalWrite(motor2_frente,LOW);
           Serial.println("Esquerda");
       
    }
    if (memcmp(MsgRecebida,CmdNodeMCU4,3) == 0) //Direita
    {
 
           digitalWrite(motor1_frente,HIGH);
           digitalWrite(motor2_frente,LOW);
           digitalWrite(motor1_tras,LOW);
           digitalWrite(motor2_tras,LOW);
           Serial.println("Direita");

    }
    if (memcmp(MsgRecebida,CmdNodeMCU7,3) == 0) //Direita para Uso Manual
    {
 
           digitalWrite(motor1_frente,HIGH);
           digitalWrite(motor2_frente,LOW);
           digitalWrite(motor1_tras,LOW);
           digitalWrite(motor2_tras,LOW);
           delay(500);
           digitalWrite(motor1_frente,LOW);
           Serial.println("Direita");

    }
    if(memcmp(MsgRecebida, CmdNodeMCU5,3) == 0) //Parar
    {
      off();     
      Serial.println("Parar");    
    }
}
  
//Função: reconecta-se ao broker MQTT (caso ainda não esteja conectado ou em caso de a conexão cair)
//        em caso de sucesso na conexão ou reconexão, o subscribe dos tópicos é refeito.
//Parâmetros: nenhum
//Retorno: nenhum
void reconnectMQTT() 
{
    //Serial.println("Conectando ao Broker");
    while (!MQTT.connected()) 
    {
        Serial.print("* Tentando se conectar ao Broker MQTT: ");
        Serial.println(BROKER_MQTT);
        if (MQTT.connect(ID_MQTT)) 
        {
            Serial.println("Conectado com sucesso ao broker MQTT!");
            MQTT.subscribe(TOPICO_SUBSCRIBE); 
        } 
        else
        {
            Serial.println("Falha ao reconectar no broker.");
            Serial.println("Havera nova tentatica de conexao em 2s");
            delay(2000);
        }
    }
}
  
//Função: reconecta-se ao WiFi
//Parâmetros: nenhum
//Retorno: nenhum
void reconectWiFi() 
{
    //se já está conectado a rede WI-FI, nada é feito. 
    //Caso contrário, são efetuadas tentativas de conexão
    if (WiFi.status() == WL_CONNECTED)
        return;
         
    WiFi.begin(SSID, PASSWORD); // Conecta na rede WI-FI
     
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(100);
        Serial.print(".");
        Serial.println("Não consigo conectar a rede wifi");
    }
   
    Serial.println();
    Serial.print("Conectado com sucesso na rede ");
    Serial.print(SSID);
    Serial.println("IP obtido: ");
    Serial.println(WiFi.localIP());
}
 
//Função: verifica o estado das conexões WiFI e ao broker MQTT. 
//        Em caso de desconexão (qualquer uma das duas), a conexão
//        é refeita.
//Parâmetros: nenhum
//Retorno: nenhum
void VerificaConexoesWiFIEMQTT(void)
{
    if (!MQTT.connected()) 
        reconnectMQTT(); //se não há conexão com o Broker, a conexão é refeita
     
     reconectWiFi(); //se não há conexão com o WiFI, a conexão é refeita
}
 
//Função: inicializa o output em nível lógico baixo
//Parâmetros: nenhum
//Retorno: nenhum
void InitOutput(void)
{
    pinMode(D0, OUTPUT);
    digitalWrite(D0, LOW);          
    EstadoSaida1 = '0';

    pinMode(D1, OUTPUT);
    digitalWrite(D1, LOW);          
    EstadoSaida2 = '0';

    pinMode(D2, OUTPUT);
    digitalWrite(D2, LOW);          
    EstadoSaida3 = '0';

    pinMode(D3, OUTPUT);
    digitalWrite(D3, LOW);          
    EstadoSaida4 = '0';
    
}
 
 
//programa principal
void loop() 
{   
    //garante funcionamento das conexões WiFi e ao broker MQTT
    VerificaConexoesWiFIEMQTT();
    //Serial.println("Iniciando ... ");
    //keep-alive da comunicação com broker MQTT
    MQTT.loop();
}
