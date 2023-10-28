import RPi.GPIO as g
import time

LED1, LED2, LED3 = 5, 6, 13
g.setmode(g.BCM)
g.setup(LED1, g.OUT)
g.setup(LED2, g.OUT)
g.setup(LED3, g.OUT)


def set_led(a=False, b=False, c=False):
    g.output(LED1, a)
    g.output(LED2, b)
    g.output(LED3, c)


try:
    while True:
        set_led(True)
        time.sleep(0.5)
        set_led(b=True)
        time.sleep(0.5)
        set_led(c=True)
        time.sleep(0.5)
finally:
    g.cleanup()
