import pygame as py
import time as tm
import sys

def test():
    screen = py.display.set_mode((1000, 700))
    getreckt = py.Rect(0, 0, 100, 100)
    py.draw.rect(screen, (255, 0, 0), getreckt)
    tm.sleep(1)
    sys.exit()