import csv
import sqlite3
from plutoGateway import PlutoGateway, PlutoGatewayChannel
import time

channels = dict()

with open("channels.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    headers = dict()
    first = True
    for row in reader:
        if first:
            for i, h in enumerate(row):
                headers[h] = i
            first = False
        else:
            name = row[headers["name"]]

            if name != "":
                channels[name] = dict()


                def intt(str):
                    try:
                        return int(str)
                    except Exception:
                        return None

                channels[name]["mb_type"] = row[headers["mb_type"]]
                channels[name]["unit_id"] = intt(row[headers["unit_id"]])
                channels[name]["permissions"] = row[headers["permissions"]]
                channels[name]["addr"] = intt(row[headers["addr"]])
                channels[name]["bit"] = intt(row[headers["bit"]])
                channels[name]["related"] = row[headers["related"]]
                channels[name]["default_value"] = row[headers["default_value"]]
                channels[name]["type"] = row[headers["type"]]
                channels[name]["boot_value"] = row[headers["boot_value"]]

                channels[name]["old"]=None
                channels[name]["value"] = None

print(channels)

gateway = PlutoGateway(channels,'localhost',502)

# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect('mydb.db')


for ch in channels.keys():
    try:
        # Get a cursor object
        cursor = db.cursor()
        print(ch)
        cursor.execute(f'''
            CREATE TABLE  {ch}(id INTEGER PRIMARY KEY, timestamp TIMESTAMP ,
                               value FLOAT)
        ''')

        db.commit()
    except Exception:
        pass

cursor = db.cursor()
n=0

while True:
    print('.')




    now = time.time()

    for ch in channels.keys():
        value = gateway.read_ch(ch)
        if value != channels[ch]['value']:
            cursor.execute(f'''INSERT INTO {ch}(timestamp, value)
                              VALUES(?,?)''', (now, value))
            channels[ch]['value']=value
            #print(ch,value)

    n+=1
    if n ==20:
        db.commit()
        n=0

