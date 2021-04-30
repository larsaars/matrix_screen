import random
import os
from time import sleep

os.system('clear')

rows, columns = os.popen('stty size', 'r').read().split()
rows, columns = int(rows), int(columns)

chars = 'abcdefghijklmnopqrstuvwxyz1234567890       #+ABCDEFGHIJKLMNOPQRSTUVXYZ'

while True:
    out = ''
    for i in range(columns - 2):
        out += random.choice(chars)

    os.system('echo "\e[1;32m ' + out + ' \e[0m"')
    sleep(0.02)
