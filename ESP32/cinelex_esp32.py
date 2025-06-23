#EN MICRO
from machine import Pin
import sys

# LEDs conectados a GPIOs: 13, 4, 12, 14
led0 = Pin(13, Pin.OUT)   # Caja 0
led1 = Pin(4, Pin.OUT)    # Caja 1
led2 = Pin(12, Pin.OUT)   # Caja 2
led3 = Pin(14, Pin.OUT)   # Caja 3

# Apagar todos al inicio
led0.value(0)
led1.value(0)
led2.value(0)
led3.value(0)

def leer_serial():
    while True:
        comando = sys.stdin.readline().strip()
        if ":" in comando:
            try:
                indice, estado = map(int, comando.split(":"))
                if indice == 0:
                    led0.value(estado)
                elif indice == 1:
                    led1.value(estado)
                elif indice == 2:
                    led2.value(estado)
                elif indice == 3:
                    led3.value(estado)
            except:
                pass

leer_serial()