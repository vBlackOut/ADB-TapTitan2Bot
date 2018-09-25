from Tools.shell import Shell
from PIL import Image

import random
import time
import sys


class Actions():
    def __init__(self):
        self.Console = Shell()

    def defaultAttackTitan(self, number_loop=10):
        self.count = 0
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        while 1:
            # fee accepte button
            self.Console.inputShell("input tap 700 1450", 30)

            # fee and attack
            self.Console.inputShell("input tap 500 400", 30, random.randint(2, 5))

            # midas
            self.Console.inputShell("input tap 500 1650", 30)

            # help heroes cluster
            self.Console.inputShell("input tap 400 1000", 30)

            # help pet gold
            self.Console.inputShell("input tap 600 900", 30)

            #self.Console.inputShell("screencap -p /sdcard/screen.png", 10000)
            #time.sleep(100)

            #self.Console.pullShell("/mnt/sdcard/screen.png", "screen.png")
            time.sleep(0.05)

            if self.count > number_loop:
                break

            print("number loop {}/{} Attack Titan \r".format(self.count, number_loop))
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
            self.count += 1

    def upgradeHeros(self, number_upgrade=10):
        self.count = 0
        # open menu heros
        self.Console.inputShell("input tap 310 1850", 30)

        #self.Console.inputShell("input tap 160 1650", 30)
        time.sleep(1)
        
        # upgrade double tap heros button
        for i in range(0, 5):
            self.Console.inputShell("input tap 900 1300", 30)
            time.sleep(0.1)

        while 1:

            if self.count == 0:
                self.Console.inputShell("input swipe 700 1650 700 1550", 30)
            else:
                self.Console.inputShell("input swipe 700 1650 700 {}".format(1555), 30)
            time.sleep(0.5)

            # upgrade double tap heros button
            for i in range(0, 5):
                self.Console.inputShell("input tap 900 1300", 30)
                time.sleep(0.1)

            # scroll up
            #self.Console.inputShell("input swipe 160 1500 160 4000", 30)
            time.sleep(0.5)
            if self.count > number_upgrade:
                break
            self.count += 1

        # scroll all up
        for i in range(0, (number_upgrade/(self.count/2))):
            self.Console.inputShell("input swipe 160 1500 160 4000", 30)
            time.sleep(0.5)

        time.sleep(0.5)
        self.Console.inputShell("input tap 310 1850", 30)
        time.sleep(2)

    def bossAttack(self):
        self.Console.pullShell("/mnt/sdcard/screen.png", "screen.png")
        imgpil = Image.open("screenshot/screen.png")

        color_main = self.Console.compute_average_image_color(imgpil)

        left = 820
        top = 32
        width = 250
        height = 100

        box = (left, top, left+width, top+height)
        crop = imgpil.crop(box)
        crop.save("screenshot/screen_crop.png", "PNG")
        time.sleep(1)

        imgpil = Image.open("screenshot/screen_crop.png")
        color_main = self.Console.compute_average_image_color(imgpil)
        if color_main == (35, 38, 33):
            print("Attack Boss Off")
            return False

        if color_main == (210, 102, 40):
            print("Attack Boss On")
            self.Console.inputShell("input tap 900 40", 30)
            return True
