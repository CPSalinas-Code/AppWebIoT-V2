#include "DHTesp.h"
#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <time.h>

 
#define DHTpin 14    //Para Sensor1 Humedad y temperatura D5 of NodeMCU is GPIO14
#define LED1pin 12
#define LED2pin 5
#define LED3pin 4
#define LED4pin 15

const int analogInPin = A0;
const char* ssid = "Molly";
const char* password = "CHANFLE2015";
const char* mqttServer = "192.168.0.118";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
char* valores;
int timezone = -5*3600;
int dst = 0;

int sensorValue = 0;  // value read from the pot (valores entre 0 y 1024)
int outputValue = 0;  // value to output to a PWM pin (valores entre 0 y 255)
float humedadSuelo;


WiFiClient espClient;
PubSubClient client(espClient);
DHTesp dht;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println();
  Serial.println("Status\tHumidity (%)\tTemperature (C)");
  
  // Autodetect is not working reliable, don't use the following line
  // dht.setup(17);
 
  // use this instead: 
  dht.setup(DHTpin, DHTesp::DHT11); //for DHT11 Connect DHT sensor to GPIO 17
  pinMode(LED1pin,OUTPUT);
  pinMode(LED2pin,OUTPUT);
  pinMode(LED3pin,OUTPUT);
  pinMode(LED4pin,OUTPUT);
  digitalWrite(LED1pin,HIGH);
  digitalWrite(LED2pin,HIGH);
  digitalWrite(LED3pin,HIGH);
  digitalWrite(LED4pin,HIGH);
  //dht.setup(DHTpin, DHTesp::DHT22); //for DHT22 Connect DHT sensor to GPIO 17

  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected()){
    Serial.println("Connecting to MQTT...");
    if(client.connect("ESP.8266Client",mqttUser,mqttPassword)){
      Serial.println("Connected to MQTT");
    }else{
      Serial.print("failed with state");
      Serial.print(client.state());
      delay(2000);
    }
  }
  configTime(timezone, dst, "pool.ntp.org", "time.nist.gov");
  Serial.println("\nWaiting for Internet Time.....");
  while (!time(nullptr)){
    Serial.print("*");
    delay(1000);
  }
  Serial.print("\nTime Response.....OK");
  
}

void callback(char* topic, byte* payload, unsigned int length){
  char numClave[3];
  String clave ="";
  String tiempo="";
  Serial.print("Message arrived in topic:");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i =0; i <length; i++){
    Serial.print((char)payload[i]);
  }
  Serial.println();
  clave = (String)((char)payload[0])+(String)((char)payload[1])+(String)((char)payload[2]);
  Serial.print("---");
  Serial.print(clave);
  Serial.print("---");
  Serial.println();
  tiempo = (String)((char)payload[3])+(String)((char)payload[4]);
  Serial.println("Automatico - Tiempo");
  Serial.println(clave);
  Serial.println(tiempo);
  if(clave=="L1E"){
    digitalWrite(LED1pin,0);
  }
  if(clave=="L1A"){
    digitalWrite(LED1pin,1);
  }
  if(clave=="L2E"){
    digitalWrite(LED2pin,0);
  }
  if(clave=="L2A"){
    digitalWrite(LED2pin,1);
  }
  if(clave=="L3E"){
    digitalWrite(LED3pin,0);
  }
  if(clave=="L3A"){
    digitalWrite(LED3pin,1);
  }
  if(clave=="L4E" && (tiempo.toInt())!=0){
    clave="";
    digitalWrite(LED4pin,0);
    delay((tiempo.toInt())*1000);
    digitalWrite(LED4pin,1);
  }
  
  
  //Serial.print((char)payload[0]);
  Serial.println();
  Serial.println("---------------------");
  
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(200);
  
  float humidity = dht.getHumidity();
  float temperature = dht.getTemperature();
 
  //print
  static char humedad[7];
  static char temperatura[7];
  static char humedadSueloStr[7];
  dtostrf(humidity, 5, 2, humedad);
  dtostrf(temperature, 5, 2,temperatura);
  time_t now = time(nullptr);
  struct tm* p_tm = localtime(&now);
  static String fecha;
  static String hora;
  static String fechaHora;
  fecha = (String)(p_tm->tm_year + 1900)+"-"+(String)(p_tm->tm_mon +1)+"-"+(String)(p_tm->tm_mday);
  hora = (String)(p_tm->tm_hour)+":"+(String)(p_tm->tm_min)+":"+(String)(p_tm->tm_sec);
  fechaHora = fecha+' '+hora;
  //Serial.print(p_tm->tm_mday);
  //Serial.print("/");
  //Serial.print(p_tm->tm_mon +1);
  //Serial.print("/");
  //Serial.print(p_tm->tm_year + 1900);
  //print
  static String valores;
  valores =(String)humedad+","+(String)temperatura+","+fechaHora;
  sensorValue = analogRead(analogInPin);
  outputValue = map(sensorValue, 0, 1024, 0, 255);
  humedadSuelo = (outputValue*100)/255; 
  dtostrf(humedadSuelo,5,2,humedadSueloStr);
  valores = valores+","+humedadSueloStr;
  
  
  //Serial.print(" ");

  //Serial.print(p_tm->tm_hour);
  //Serial.print(":");
  //Serial.print(p_tm->tm_min);
  //Serial.print(":");
  //Serial.println(p_tm->tm_sec);
  static char valoresChar[37];
  valores.toCharArray(valoresChar,37);  
  if((String)(p_tm->tm_sec)=="30" || (String)(p_tm->tm_sec)=="0"){
    
    Serial.print(dht.getStatusString());
    Serial.print("\t");
    Serial.print(humidity, 1);
    Serial.print("\t\t");
    Serial.print(temperature, 1);
    Serial.println();


    
    Serial.println(fecha);
    Serial.println(hora);
    Serial.println(fechaHora);

    
  
    client.publish("esp8266prueba",valoresChar);  
    delay(1000);
    
  }
  
  client.subscribe ("esp8266prueba");
  
  client.loop();
}
