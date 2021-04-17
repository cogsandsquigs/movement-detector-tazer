from time import sleep
import serial

with open("config.txt", "r") as reader:
    conts = reader.readlines()

try:
    ser = serial.Serial(conts[0], 9600)
except:
    from config import *


def encourage(data):
    if data == 0:
        ser.write(str(chr(33)).encode())
        sleep(0.1)
    if data == 1:
        ser.write(str(chr(34)).encode())
        sleep(0.1)
