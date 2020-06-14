# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from datetime import datetime

#imports lcd
from helpers.HD44780 import HD44780
from subprocess import check_output

import serial
import time
import threading
import json
import spidev

#playing sounds
import os
import pygame

# Code voor led
from helpers.MCP3008 import MCP3008
from RPi import GPIO

led1 = 21

lcd_RS = 21
lcd_E = 20
databits = [13, 19, 26, 23, 24, 25, 12, 16]

selectedmap = "piano"

mcp = MCP3008()

#GPIO.output(lasers, GPIO.LOW)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

endpoint = "/api/v1"

@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_select_sound')
def switch_sound(data):
    global selectedmap
    selectedmap = data['selected_sound']
    print(selectedmap)

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/playhistory/<user_id>')
def get_playhistory(user_id):
    print(user_id)
    if request.method == 'GET':
        print(user_id)
        s = DataRepository.get_historiek(user_id)
        return jsonify(s), 200

@app.route(endpoint + '/decibelmeter/live')
def get_live_decibelmeter():
    if request.method == "GET":
        s = DataRepository.get_live_decibels()
        return jsonify(s), 200

def read_all_ldrs():
    while True:
        # C noot => laser 1
        channelC = mcp.read_channel(0)
        if channelC > 500:
            play_note("C",selectedmap)

        # D noot => laser 2
        channelD = mcp.read_channel(1)
        if channelD > 500:
            play_note("D",selectedmap)

        # E noot => laser 3
        channelE = mcp.read_channel(2)
        if channelE > 500:
            play_note("E",selectedmap)

        # F noot => laser 4
        channelF = mcp.read_channel(3)
        if channelF > 500:
            play_note("F",selectedmap)

        # G noot => laser 5
        channelG = mcp.read_channel(4)
        if channelG > 500:
            play_note("G",selectedmap)

        # A noot => laser 6
        channelA = mcp.read_channel(5)
        if channelA > 500:
            play_note("A",selectedmap)
        # B noot => laser 2
        channelB = mcp.read_channel(6)
        if channelB > 500:
            play_note("B",selectedmap)

        #threading.Timer(1, read_all_ldrs(selectedmap)).start()

        # print(f"Channel C: {channelC}")
        # print(f"Channel D: {channelD}")
        # print(f"Channel E: {channelE}")
        # print(f"Channel F: {channelF}")
        # print(f"Channel G: {channelG}")
        # print(f"Channel A: {channelA}")
        # print(f"Channel B: {channelB}")


def play_note(activatedNote, selectedmap):
    # print(activatedNote)
    # print(f"/home/robbe/1920-1mct-project1-RaevensRobbe/Code/backend/sounds/{selectedmap}/{activatedNote}.wav")
    sound = pygame.mixer.Sound(f"/home/robbe/1920-1mct-project1-RaevensRobbe/Code/backend/sounds/{selectedmap}/{activatedNote}.wav")
    sound.play()
    # while pygame.mixer.get_busy():
    #     print(pygame.mixer.get_busy())
    #     pass

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    #voor de sounds
    pygame.init()
    pygame.mixer.init()

def databasefunctie():
    #voor de sounds
    pygame.init()
    pygame.mixer.init()

    setup()
    #LCD instellen
    lcd = HD44780(lcd_RS, lcd_E, databits)
    lcd.init_LCD()
    ips = check_output(["hostname", "--all-ip-addresses"])
    print(ips)
    ips = str(ips)
    ip = ips.strip("b'").split(" ")
    print(ip[1])
    lcd.send_instruction(0x01)
    lcd.write_message(str(ip[1]))

    #serial communicatie arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    #variabelen
    i = 0
    tijd = ""
    userID = ""
    print("scan to start")
    while True:
        value = ser.readline().decode().rstrip()
        uid_scanned = value[:4]
        print(value)
        if uid_scanned == "UID:" and i == 0:
            i = 1
            print("RFID SCANNED")
            uid = value[5:]
            print(f"RFID UID: {uid}")
            status = DataRepository.get_user(uid)
            userID = status['UserID']
            print(f"UserID: {userID}")
            now = datetime.now()
            tijd = now.strftime("%H:%M:%S")
            datum = now.strftime("%Y-%m-%d %H:%M:%S")
            play_note("start",'startstop')
            insert = DataRepository.insert_historiek_play(userID, datum)
            lcd.send_instruction(lcd.secondline())
            lcd.write_message(str(f"{value}   "))
            time.sleep(2)
            #GPIO.output(lasers, GPIO.HIGH)
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
            play_note("stop",'startstop')
            time.sleep(5)
            #GPIO.output(lasers, GPIO.LOW)
        elif i == 1:
            lcd.send_instruction(lcd.secondline())
            lcd.write_message(str(f"{value} dB             "))
            if value != '-INF':
                insert_decibel = DataRepository.insert_decibels(value)
            #databasewaarde = DataRepository.get_live_decibels()
        elif i == 0 and uid_scanned != "UID:":
            lcd.send_instruction(lcd.secondline())
            lcd.write_message(str(f"{value} dB             "))

def startserver():
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)

threading.Timer(1, databasefunctie).start()
threading.Timer(2, startserver).start()
threading.Timer(1, read_all_ldrs()).start()
print("testtttttttttttttttttttt")




if __name__ == '__main__':
    # pass
    # socketio.run(app, debug=False, host='0.0.0.0', port=5000)
    try:
        pass    

    except KeyboardInterrupt as ex:
        print(ex)
        GPIO.cleanup()
    finally:
        GPIO.cleanup() 
