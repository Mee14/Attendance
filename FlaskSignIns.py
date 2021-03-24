from flask import Flask

import mysql.connector

mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password",
      database="attendance"
)
mycursor = mydb.cursor()
app = Flask(__name__)
@app.route("/")
def home():
    
    table = "<table border = 1 style=\"width:250\">\n<tr>\n<th>RFID</th>\n<th>Name</th>\n<th>Time</th>\n</tr>\n"
    
    mycursor.execute("SELECT RFID, Name, Time FROM students order by Time desc limit 5")
    fetchResult = mycursor.fetchall()
    for i in fetchResult:
        print(i)
        table = table + "<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>".format(i[0],i[1], i[2])
        
        
    return table

###########################################################
if __name__=='__main__':
    app.run()
