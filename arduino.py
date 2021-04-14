import threading
import serial

import const
from helpers import d

s = None
stop_threads = False


def init_serial():
    global s
    s = serial.Serial(const.ARDUINO_PORT, const.ARDUINO_BAUDRATE, timeout=const.ARDUINO_TIMEOUT)


def set_default_value(key, val):
    if key == 'COLOR_RED':
        const.CURRENT_COLOR[0] = val
    elif key == 'COLOR_GREEN':
        const.CURRENT_COLOR[1] = val
    elif key == 'COLOR_BLUE':
        const.CURRENT_COLOR[2] = val
    elif key == 'MODE':
        const.CURRENT_MODE = val
    elif key == 'BRIGHTNESS':
        const.CURRENT_BRIGHTNESS = val
    elif key == 'SPEED':
        const.CURRENT_SPEED = val
    elif key == 'MICROPHONE_MODE':
        const.CURRENT_MICROPHONE_MODE = val


def parseLine(line):
    if len(line) and line[0] == "@":
        v = line[1:].split(": ")
        set_default_value(v[0], int(v[1]))
    d(line)


def receive():
    global s
    line = ""
    while True:
        if stop_threads:
            break

        for b in s.read():
            if b == b"":
                continue

            c = chr(b)

            if c == "\n":
                parseLine(line)
                line = ""
            elif c != "\r":
                line += c


def send(cmd):
    d("> %s" % cmd)
    s.write((cmd + "\n").encode())


def start_reading_loop():
    t = threading.Thread(target=receive)
    t.start()
    send("v")


def stop():
    global stop_threads
    stop_threads = True
