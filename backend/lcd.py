from RPi import GPIO
import time


#imports lcd
from helpers.HD44780 import HD44780
from subprocess import check_output

lcd_RS = 21
lcd_E = 20
# databits = [16, 12, 25, 24, 23, 26, 19, 13]
databits = [13, 19, 26, 23, 24, 25, 12, 16]

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

if __name__ == '__main__':
    try:
        setup()
        #LCD instellen
        lcd = HD44780(lcd_RS, lcd_E, databits)
        lcd.init_LCD()
        while True:        
            ips = check_output(["hostname", "--all-ip-addresses"])
            ips = str(ips)
            ip = ips.strip("b'").split(" ")
            print(ip[0])
            lcd.send_instruction(0x01)
            lcd.write_message(str(ip[0]))
            time.sleep(0.3)

    except KeyboardInterrupt as ex:
        print(ex)
        GPIO.cleanup()
    finally:
        GPIO.cleanup() 
