#include "DHTesp.h"
#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <time.h>

 
#define DHTpin 14    //D15 of ESP32 DevKit
#define LED1pin 5
#define LED2pin 4


const char* ssid = "Molly";
const char* password = "CHANFLE2015";
const char* mqttServer = "192.168.0.118";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = ""; 
int timezone = -5*3600;
int dst = 0;


WiFiClient espClient;
PubSubClient client(espClient);
DHTesp dht;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println();
  Serial.println("Status\tHumidity (%)\tTemperature (C)\t(F)\tHeatIndex (C)\t(F)");

  dht.setup(DHTpin, DHTesp::DHT22); //for DHT22 Connect DHT sensor to GPIO 17
  pinMode(LED1pin,OUTPUT);
  pinMode(LED2pin,OUTPUT);
  digitalWrite(LED1pin,HIGH);
  digitalWrite(LED2pin,HIGH);

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
    if(client.connect("ESP.8266Client_PB",mqttUser,mqttPassword)){
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
  Serial.print("Message arrived in topic:");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i =0; i <length; i++){
    Serial.print((char)payload[i]);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  //delay(dht.getMinimumSamplingPeriod());
  delay(200);
 
  float humidity = dht.getHumidity();
  float temperature = dht.getTemperature();
  static char humedad[7];
  static char temperatura[7];
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

  static String valores;
  valores =(String)humedad+","+(String)temperatura+","+fechaHora;

  static char valoresChar[33];
  valores.toCharArray(valoresChar,33);  
  if((String)(p_tm->tm_sec)=="15"){
    
    Serial.print(dht.getStatusString());
    Serial.print("\t");
    Serial.print(humidity, 1);
    Serial.print("\t\t");
    Serial.print(temperature, 1);
    Serial.println();


    
    Serial.println(fecha);
    Serial.println(hora);
    Serial.println(fechaHora);

    
  
    client.publish("plantabaja/nodemcu",valoresChar);  
    delay(1000);
    
  }
  
  client.subscribe ("plantabaja/nodemcu");
  
  client.loop();
  //Serial.print(dht.getStatusString());
  //Serial.print("\t");
  //Serial.print(humidity, 1);
  //Serial.print("\t\t");
  //Serial.print(temperature, 1);
  //Serial.println();

}
