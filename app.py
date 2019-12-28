from flask import Flask, redirect, request, json
from flask import render_template, Response, url_for
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json
import time
import threading
import datetime
import pymysql

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
fechaINICIAL = ""
fechaFINAL = ""
temp, fecha = [],[]
Ltemperatura, Lfecha=[],[]
listaDatos = []
listaDatosFecha = []
conn = pymysql.connect(host="localhost",user="admin",passwd="",db="BD1")
listaFechasActividades=[]
listaFechasActividadesF=[]
status, statusL = [],[]
idd=[]

mqtt_topic = "esp8266prueba"
mqtt_broker_ip ="192.168.0.118"

client = mqtt.Client()

def consulta(fecha_I, fecha_F, hora_I, hora_F):
    try:
        mysql_consult_query = "SELECT temperatura, fechaHora FROM Sensor1 WHERE fechaHora>"+"\'"+fecha_I+" "+hora_I+":00"+"\'"+" AND fechaHora<="+"\'"+fecha_F+" "+hora_F+":00"+"\'"+";";
        #conn = pymysql.connect(host="localhost",user="admin",passwd="",db="BD1")
        cursor= conn.cursor()
        print (mysql_consult_query)
        cursor.execute(mysql_consult_query) 
        rows = cursor.fetchall()
        print('total rows:', cursor.rowcount)
        for row in rows:
            temp.append(row[0])
            fecha.append(row[1])
        for tempe in temp:
            Ltemperatura.append(float(tempe))
        for fech in fecha:
            Lfecha.append(str(fech))
    except: 
        print ('Error: unable to fetch data')
    cursor.close()

@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/controlDisp.html")
def control():
    return render_template("controlDisp.html")


@app.route("/help.html")
def help():
    return render_template("help.html")

@app.route("/proAutomatica.html", methods=['POST'])
def getValueProgra():
    fechaProgra = request.form['fechaActivacion']
    horaProgra = request.form['horaActivacion']
    opcionProgra = request.form['opcion']
    horaProgra = horaProgra+":00"
    opcionSegundos = request.form['opcionSegundos']
    print(fechaProgra)
    print(horaProgra)
    print(opcionProgra)
    print(opcionSegundos)
    guardarPrograAuto(fechaProgra,horaProgra,opcionProgra,opcionSegundos)
    data = getPrograAuto()
    return render_template("proAutomatica.html",datos=data)


def guardarPrograAuto(fecha, hora, opcion, segundos):
    mysql_insert_queryP = ""
    if(opcion=="1"):
        print("opcion 1")
        fechaHoraP= fecha+" "+hora
        mysql_insert_queryP = "INSERT INTO ProgramacionAuto (sensor,fechaHoraProgra,status,segundos) VALUES ('Sensor1',"+"\'"+fechaHoraP+"\'"+","+"\'"+"Activo"+"\'"+","+segundos+");"
        print(mysql_insert_queryP)
        try:
            cursor= conn.cursor();
            cursor.execute(mysql_insert_queryP)
            mysql_consult_queryAct="SELECT fechaHoraProgra,segundos,idPrograAuto FROM ProgramacionAuto WHERE status="+"\'"+"Activo"+"\'"+";"                  
            cursor.execute(mysql_consult_queryAct)
            rows = cursor.fetchall()
            print('total fechas actividades:', cursor.rowcount)
            for row in rows:
                listaFechasActividades.append(row[0])
                status.append(str(row[1]))
                idd.append(str(row[2]))
            for fech in listaFechasActividades:
                listaFechasActividadesF.append(str(fech))
            cursor.close()
            time.sleep(2)
            conn.commit();
            
            print ("Insertado con Exito en Tabla PrograAuto")
        except:
            print ('Error al insertar en tabla PrograAuto: ')
    elif(opcion=="7"):
        print("opcion 7")
    print("salir")

@app.route("/historial.html")
def historial():
    return render_template("historial.html")

@app.route("/historial.html", methods=['POST'])
def getValue():
    legend = "Temperatura"
    fechaInicio = request.form['fechaINICIAL']
    fechaFinal = request.form['fechaFINAL']
    horaInicio = request.form['horaINICIAL']
    horaFinal = request.form['horaFINAL']
    consulta(fechaInicio, fechaFinal, horaInicio, horaFinal)
    #print(Ltemperatura)
    #print(Lfecha)
    #return render_template("historial.html", legend=legend F_INICIAL=fechaInicio, F_FINAL=fechaFinal, listtemp=json.dumps(Ltemperatura), listfecha=json.dumps(Lfecha))
    return render_template("historial.html", legend=legend, F_INICIAL=fechaInicio, F_FINAL=fechaFinal, values=Ltemperatura, labels=Lfecha)


@app.route("/proAutomatica.html/delete/<string:id>")
def delete_contact(id):
    mysql_consult_queryEliminar="DELETE FROM ProgramacionAuto WHERE idPrograAuto = {0};".format(id)
    cursor= conn.cursor()
    cursor.execute(mysql_consult_queryEliminar)
    conn.commit()
    data = getPrograAuto()
    return render_template("proAutomatica.html", datos=data)

def getPrograAuto():
    mysql_consult_queryAuto="SELECT * FROM ProgramacionAuto;"
    cursor= conn.cursor()
    cursor.execute(mysql_consult_queryAuto)
    datax = cursor.fetchall()
    return datax

@app.route("/proAutomatica.html")
def programacion():
    data = getPrograAuto()
    return render_template("proAutomatica.html", datos=data)

@app.route("/datepicker.html")
def datepicker():
    return render_template("datepicker.html")

@app.route('/Lamp1')
def Lamp1():
    return render_template('controlDisp.html')

@app.route('/LlamarEncenderL1', methods=['POST'])
def LlamarEncenderL1():
    client.publish("esp8266prueba","L1E")
    #GPIO.output(17,GPIO.HIGH)
    return json.dumps({'status':'Llamando Encender L1'});

@app.route('/LlamarApagarL1', methods=['POST'])
def LlamarApagarL1():
    client.publish("esp8266prueba","L1A")
    #GPIO.output(17,GPIO.LOW)
    return json.dumps({'status':'Llamando Apagar L1'});

@app.route('/LlamarEncenderL2', methods=['POST'])
def LlamarEncenderL2():
    client.publish("esp8266prueba","L2E")
    #GPIO.output(27,GPIO.HIGH)
    return json.dumps({'status':'Llamando Encender L2'});

@app.route('/LlamarApagarL2', methods=['POST'])
def LlamarApagarL2():
    client.publish("esp8266prueba","L2A")
    #GPIO.output(27,GPIO.LOW)
    return json.dumps({'status':'Llamando Apagar L2'});

@app.route('/LlamarEncenderL3', methods=['POST'])
def LlamarEncenderL3():
    client.publish("esp8266prueba","L3E")
    #GPIO.output(22,GPIO.HIGH)
    return json.dumps({'status':'Llamando Encender L3'});

@app.route('/LlamarApagarL3', methods=['POST'])
def LlamarApagarL3():
    client.publish("esp8266prueba","L3A")
    #GPIO.output(22,GPIO.LOW)
    return json.dumps({'status':'Llamando Apagar L3'});

def consultar():
    while True:
        time.sleep(1.1)
        #x2="2019-12-16 23:00:00"
        x = str(datetime.datetime.now())
        x2 = x[0:19]
        x=0
        mensaje=""
        for fecha in listaFechasActividades:
            #print(fecha)
            if(x2==str(fecha)):
                print("SI coincide")
                mensaje = "L4E"+status[x]
                print(mensaje)
                client.publish("esp8266prueba",mensaje)
                marcarActividadRealizada(idd[x])
                time.sleep(10)
                break
            x+=1
            
        
def marcarActividadRealizada(idActividad):
    mysql_consult_queryAct="UPDATE ProgramacionAuto SET status="+"\'"+"Hecho"+"\'"+" WHERE idPrograAuto="+idActividad+";"                  
    cursor= conn.cursor()
    cursor.execute(mysql_consult_queryAct)
    conn.commit()
    actualizarActividades()
    print("Actividades Actualizadas")
    consultar()
    
        
def actualizarActividades():
    mysql_consult_queryAct="SELECT fechaHoraProgra,segundos,idPrograAuto FROM ProgramacionAuto WHERE status="+"\'"+"Activo"+"\'"+";"                  
    cursor= conn.cursor()
    cursor.execute(mysql_consult_queryAct)
    rows = cursor.fetchall()
    print('total fechas actividades:', cursor.rowcount)
    for row in rows:
        listaFechasActividades.append(row[0])
        status.append(str(row[1]))
        idd.append(str(row[2]))
    for fech in listaFechasActividades:
        listaFechasActividadesF.append(str(fech))
    #print(str(listaFechasActividadesF))
    #print(status)
        
def myfunction(client, userdata,flags, rc):
    print ("Connected!", str(rc))
    client.subscribe(mqtt_topic)
    time.sleep(1.1)
    
def on_message(client, userdata, msg):
    listaDatos = (str(msg.payload))[2:].split(",")
    listaDatos[2]=listaDatos[2].rstrip("'")
    listaDatosFecha = listaDatos[2].split(" ")
    mysql_insert_query = ""
    mysql_insert_query = "INSERT INTO Sensor1 (NombreSensor,temperatura,humedad,fecha,hora,fechaHora) VALUES ('Sensor1',"+listaDatos[1]+","+listaDatos[0]+","+"\'"+listaDatosFecha[0]+"\'"+","+"\'"+listaDatosFecha[1]+"\'"+","+"\'"+listaDatos[2]+"\'"+");"
    try:
        #conn = pymysql.connect(host="localhost",user="admin",passwd="",db="BD1")
        cursor= conn.cursor();
        print (mysql_insert_query)
        cursor.execute(mysql_insert_query)
        cursor.close()
        time.sleep(2)
        conn.commit();
        print ("Insertado con Exito")
    except Error as e:
        print ('Error: ',e)

if __name__ == "__main__":
    client.on_connect = myfunction
    client.on_message = on_message
    t1 = threading.Thread(name="Hilo_tiempo",target=consultar)
    t1.start()
    t2 = threading.Thread(name="Hilo_fechas_act",target=actualizarActividades)
    t2.start()    
    client.connect(mqtt_broker_ip,1883)
    t3 = threading.Thread(name="Hilo_fechass_act",target=client.loop_start())
    t3.start()
    time.sleep(5)
    t4 = threading.Thread(name="Hilso_fechass_act",target=app.run(host = '0.0.0.0',port=5380))
    t4.start()
    client.disconnect()
    client.loop_stop()
    
    
    
    
    
    
    
    

    