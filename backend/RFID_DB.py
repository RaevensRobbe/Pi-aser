# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

from datetime import datetime
import serial
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    i = 0
    tijd = ""
    userID = ""
    print("scan to start")
    while True:
        value = ser.readline().decode().rstrip()
        uid_scanned = value[:4]
        if uid_scanned == "UID:" and i == 0:
            i = 1
            print(f"RFID SCANNED")
            uid = value[6:]
            print(f"RFID UID: {uid}")
            status = DataRepository.get_user(uid)
            userID = status['UserID']
            print(f"UserID: {userID}")
            now = datetime.now()
            tijd = now.strftime("%H:%M:%S")
            datum = now.strftime("%Y-%m-%d %H:%M:%S")
            insert = DataRepository.insert_historiek_play(userID, datum)
        elif uid_scanned == "UID:" and i == 1:
            i = 0
            print("2E SCAN OM AF TE SLUITEN")
            print(userID, tijd)
            now = datetime.now()
            Formaat = '%H:%M:%S'
            tijdnu = now.strftime(Formaat)
            playtime = datetime.strptime(tijdnu, Formaat) - datetime.strptime(tijd, Formaat)
            print(playtime)
            update = DataRepository.update_historiek_play(playtime, datum) 
        elif i ==1:
            insert_decibel = DataRepository.insert_decibels(value)
            databasewaarde = DataRepository.get_live_decibels()
            print(f"Live: {databasewaarde}")