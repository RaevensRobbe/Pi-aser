# pylint:skip-file
import time
from RPi import GPIO


class HD44780:
    def __init__(self, lcd_RS, lcd_E, databits):
        self.lcd_RS = lcd_RS
        self.lcd_E = lcd_E
        self.databits = databits
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.lcd_RS, GPIO.OUT)
        GPIO.setup(self.lcd_E, GPIO.OUT)
        for databit in self.databits:
            GPIO.setup(databit, GPIO.OUT)

    def init_LCD(self):
        self.send_instruction(0x3C)
        self.send_instruction(0x0F)
        self.send_instruction(0X01)

    def set_data_bits(self, number):
        for bit in range(0, 8):
            GPIO.output(self.databits[bit], 0x80 & (number << bit))

    def send_instruction(self, number):
        GPIO.output(self.lcd_RS, GPIO.LOW)
        GPIO.output(self.lcd_E, GPIO.HIGH)
        self.set_data_bits(number)
        GPIO.output(self.lcd_E, GPIO.LOW)
        time.sleep(0.01)

    def send_character(self, letter):
        GPIO.output(self.lcd_RS, GPIO.HIGH)
        GPIO.output(self.lcd_E, GPIO.HIGH)
        self.set_data_bits(letter)
        GPIO.output(self.lcd_E, GPIO.LOW)
        time.sleep(0.01)

    def write_message(self, woord):
        for letter in woord:
            self.send_character(ord(letter))

    def secondline(self):
        DDRAM = 0b10000000 | 0x40
        return DDRAM
