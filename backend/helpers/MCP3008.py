import spidev
import time

class MCP3008:
    def __init__(self, bus=0, device=0):     
        self.spi = spidev.SpiDev() # spidev initialiseren
        self.spi.open(bus, device) # bus 0 en device 0 openzetten
        self.spi.max_speed_hz = 10 ** 5 # klokfrequentie instellen op 100 hz

    def read_channel(self, ch):
        # commandobyte samenstellen
        channel = ch << 4 | 128
        #list maken omdat je bij spi.xfer een list nodig hebt
        bytes_xfer = [0b00000001, channel, 0b00000000]
        #waardes bekijken die ingegeven zijn
        value_channel = self.spi.xfer(bytes_xfer)
        byte1 = value_channel[1]
        byte2 = value_channel[2]
        result_channel = byte1 << 8 | byte2
        return result_channel