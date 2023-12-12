import threading

from mfrc522 import SimpleMFRC522
import RPi.GPIO as g
import serial
import time

g.setmode(g.BCM)

RED_LED = 20
GREEN_LED = 21
BUZZER = 5
BUZZER2 = 18
SW = 16
TRIG, ECHO = 24, 23
STEPPER_PINS_X = [4, 17, 27, 22]
STEPPER_PINS_Y = [6, 13, 19, 26]
CARD_ID = [15646238359]

JOY_STICK_MIN = 400
JOY_STICK_MAX = 700

seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

for pin in STEPPER_PINS_X:
    g.setup(pin, g.OUT)
    g.output(pin, 0)

for pin in STEPPER_PINS_Y:
    g.setup(pin, g.OUT)
    g.output(pin, 0)

g.setup(BUZZER, g.OUT)
g.setup(RED_LED, g.OUT)
g.setup(GREEN_LED, g.OUT)
g.setup(SW, g.IN)
g.setup(TRIG, g.OUT)
g.setup(ECHO, g.IN)
g.setup(BUZZER2, g.OUT)

ser = serial.Serial("/dev/ttyUSB0", 9600)
ser1 = serial.Serial("/dev/ttyUSB1", 9600)
buzz = g.PWM(BUZZER, 440)
buzz2 = g.PWM(BUZZER2, 440)
rfid = SimpleMFRC522()


def send_command(is_open):
    command = "True" if is_open else "False"
    ser1.write((command + '\n').encode())
    time.sleep(1)


def set_led(red: bool = False, green: bool = False):
    g.output(RED_LED, red)
    g.output(GREEN_LED, green)


def motor_left(pins: list):
    for s in range(8):
        for p in range(4):
            g.output(pins[p], seq[7 - s][p])
        time.sleep(0.001)


def motor_right(pins: list):
    for s in range(8):
        for p in range(4):
            g.output(pins[p], seq[s][p])
        time.sleep(0.001)


# 초음파 센서
def length():
    global distance
    while True:
        g.output(TRIG, g.LOW)
        time.sleep(0.00001)
        g.output(TRIG, g.HIGH)
        start, stop = 0, 0
        while g.input(ECHO) == 0:
            start = time.time()
        while g.input(ECHO) == 1:
            stop = time.time()
        distance = (stop - start) * (34000 / 2)
        print("%.2f cm" % distance)
        time.sleep(0.2)
        if 40 >= distance > 25:
            buzz2.start(50)
            buzz2.ChangeFrequency(523)
            time.sleep(0.3)
            buzz2.stop()
            time.sleep(0.3)

        elif 25 >= distance > 10:
            buzz2.start(50)
            buzz2.ChangeFrequency(523)
            time.sleep(0.15)
            buzz2.stop()
            time.sleep(0.1)

        elif distance <= 10:
            buzz2.start(99)
            buzz2.ChangeFrequency(523)
            time.sleep(0.05)
            buzz2.stop()
            time.sleep(0.05)
        else:
            buzz2.stop()
            time.sleep(0.5)


distance = 0
thread = threading.Thread(target=length)

try:
    set_led()
    isStart = False
    # 카드 인식
    while not isStart:
        rfId = rfid.read_id()
        print(rfId)
        time.sleep(0.05)
        if rfId in CARD_ID:
            break
        else:
            set_led(red=True)
            buzz.start(50)
            time.sleep(1)
            buzz.stop()
    # 카드 통과하였을때
    set_led(green=True)
    # 실행
    check = False  # 집게를 집을때 true, 집게 펼칠때 false
    thread.start()
    while True:
        if g.input(SW):
            check = not check
            threading.Thread(target=send_command, args=tuple([check])).start()
            time.sleep(0.5)
        line = ser.readline()
        x, y = map(int, str(line, 'utf-8', 'ignore').strip().split())
        if not JOY_STICK_MIN < x < JOY_STICK_MAX:
            if x < JOY_STICK_MIN:
                motor_left(STEPPER_PINS_X)
            elif x > JOY_STICK_MAX:
                motor_right(STEPPER_PINS_X)
        if not JOY_STICK_MIN < y < JOY_STICK_MAX:
            if y < JOY_STICK_MIN:
                motor_left(STEPPER_PINS_Y)
            elif y > JOY_STICK_MAX:
                motor_right(STEPPER_PINS_Y)
finally:
    g.cleanup()
