import pymysql

conn = pymysql.connect(host="localhost",user="admin",passwd="",db="BD1")
cursor= conn.cursor()
temp, fecha = [],[]

F_INICIAL = "2019-12-13"
F_FINAL = "2019-12-14"
#mysql_insert_query = "INSERT INTO Sensor1 (NombreSensor,temperatura,humedad,fecha,hora,fechaHora) VALUES ('Sensor1',"+listaDatos[1]+","+listaDatos[0]+","+"\'"+listaDatosFecha[0]+"\'"+","+"\'"+listaDatosFecha[1]+"\'"+","+"\'"+listaDatos[2]+"\'"+");"
mysql_consult_query = "SELECT temperatura, fecha FROM Sensor1 WHERE fecha>"+"\'"+F_INICIAL+"\'"+" AND fecha<="+"\'"+F_FINAL+"\'"+";";



try:
    print (mysql_consult_query)
    cursor.execute(mysql_consult_query) 
    rows = cursor.fetchall()
    print('total rows:', cursor.rowcount)
    
    for row in rows:
        temp.append(row[0])
        fecha.append(row[1])
except: 
    print ('Error: unable to fetch data')
        
conn.close()

def remove_char(s):
    return s[ 1:- 1]