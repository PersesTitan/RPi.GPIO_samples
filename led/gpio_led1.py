import RPi.GPIO as g

LED1 = 5
g.setmode(g.BCM)
g.setup(LED1, g.OUT)

try:
    g.output(LED1, True)
    input()
finally:
    g.cleanup()