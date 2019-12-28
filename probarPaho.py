
import paho.mqtt.client as mqtt
import pymysql


mqtt_topic = "esp8266prueba"
mqtt_broker_ip ="192.168.0.118"
listaDatos = []
listaDatosFecha = []
conn = pymysql.connect(host="localhost",user="admin",passwd="",db="BD1")
cursor= conn.cursor();

client = mqtt.Client()
def on_connect(client, userdata,flags, rc):
    print ("Connected!", str(rc))
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    listaDatos = (str(msg.payload))[2:].split(",")
    listaDatos[2]=listaDatos[2].rstrip("'")
    listaDatosFecha = listaDatos[2].split(" ")
    mysql_insert_query = ""
    mysql_insert_query = "INSERT INTO Sensor1 (NombreSensor,temperatura,humedad,fecha,hora,fechaHora) VALUES ('Sensor1',"+listaDatos[1]+","+listaDatos[0]+","+"\'"+listaDatosFecha[0]+"\'"+","+"\'"+listaDatosFecha[1]+"\'"+","+"\'"+listaDatos[2]+"\'"+");"
    #probar = """INSERT INTO probar (nombres)""" \
           #  """VALUES (%s)"""
    #x = [('holla')]
    #print (probar)
    try:
        cursor= conn.cursor();
        print (mysql_insert_query)
        cursor.execute(mysql_insert_query)
        conn.commit();
        cursor.close()
        print ("Insertado con Exito")
    except Error as e:
        print ('Error: ',e)
        #cursor.close()
        #conn.close()
    #print (str(msg.payload))
    #print (listaDatos[0])
    #print (listaDatos[1])
    #print (listaDatos[2])
    
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip,1883)
client.loop_forever()
client.disconnect()