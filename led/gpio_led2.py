import RPi.GPIO as g
import time

LED1 = 5
g.setmode(g.BCM)
g.setup(LED1, g.OUT)

try:
    while True:
        g.output(LED1, True)
        time.sleep(0.5)
        g.output(LED1, False)
        time.sleep(0.5)
finally:
    g.cleanup()
