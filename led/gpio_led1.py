import RPi.GPIO as g
import time

LED1 = 5
g.setmode(g.BCM)
g.setup(LED1, g.OUT)

try:
    g.output(LED1, True)
    while True:
        time.sleep(0.5)
finally:
    g.cleanup()
