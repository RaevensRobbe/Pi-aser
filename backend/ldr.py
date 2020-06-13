from helpers.MCP3008 import MCP3008
from RPi import GPIO

mcp = MCP3008()

while True:
    channelC = mcp.read_channel(8)
    print(channelC)