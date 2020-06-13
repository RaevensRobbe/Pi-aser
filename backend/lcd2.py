# pylint:skip-file
import time
from RPi import GPIO
from helpers.HD44780 import HD44780
GPIO.setwarnings(False)
lcd_RS = 21
lcd_E = 20
databits = [13, 19, 26, 23, 24, 25, 12, 16]
lcd = HD44780(lcd_RS, lcd_E, databits)
if __name__ == "__main__":
    try:
        lcd.init_LCD()
        menu = ''
        inst = ''
        zin = ''
        while menu.upper() != 'X':
            menu = input("I voor input, S voor settings X to quit> ")
            if menu.upper() == 'I':
                while zin.upper() != 'T':
                    zin = input(
                        "Geef een zin/woord | druk T om terug te gaan: ")
                    if(zin.upper() != "T"):
                        lcd.send_instruction(0x01)
                        if len(zin) > 16 and len(zin) <= 32:
                            lcd.write_message(str(zin[:16]))
                            lcd.send_instruction(0xC0)
                            lcd.write_message(str(zin[16:]))
                        elif len(zin) < 16 and len(zin) <= 32:
                            lcd.write_message(str(zin))
                    else:
                        lcd.send_instruction(1)
                zin = ''
            elif menu.upper() == 'S':
                while inst.upper() != 'T':
                    inst = input(
                        "Settings: Zet blink aan of uit. Druk T om terug te gaan:> ")
                    if (inst.lower() == 'aan'):
                        lcd.send_instruction(0x0F)
                    elif (inst.lower() == 'uit'):
                        lcd.send_instruction(0x0E)
                    else:
                        print('Geef aan of uit in')

        # send_character()
    except KeyboardInterrupt:
        print("Stop")
    finally:
        print("Finally")