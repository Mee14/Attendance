import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import time

reader = SimpleMFRC522()

lcd = CharLCD('PCF8574', 0x27)
mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password",
      database="attendance"
)
mycursor = mydb.cursor()

#########################################################
def createTable():
    mycursor.execute("CREATE TABLE IF NOT EXISTS students(RFID TEXT, Name TEXT, Time Timestamp)")




def exist(RFID, Name):#write
    query = "SELECT count(*) FROM students where RFID ='{}' and Time = Now()".format(RFID)
    
    mycursor.execute(query)
    
    myresult = mycursor.fetchall()
    
    count = myresult[0][0]
    
    if count == 0:
        sql = "INSERT INTO students (RFID, Name, Time) VALUES (%s, %s, Now())"
        val = (RFID, Name)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        
        
def Scann():
    lcd.write_string("Put yo card on")
    
    
    id, text = reader.read()
    x = text.strip()
    exist(id, x)
    
    lcd.clear()
    data = text.strip()
    lcd.write_string("\r\nName: " + data)
    sql = "SELECT Name, Time from students order by Time desc limit 5"
    
    mycursor.execute(sql)
    for i in mycursor:
        print(i)
    mydb.commit()
    print("\n\n\n")
    time.sleep(3)
    lcd.clear()
    Scann()

createTable()
try:  
    Scann()
    
    print("Read")
        
finally:
    GPIO.cleanup()
    
######################################################
