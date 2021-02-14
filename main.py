import os
from time import sleep
from pynput import keyboard
from colorama import Style, Fore, init
import ctypes
import msvcrt
import subprocess
from ctypes import wintypes
import random

os.system('cls')
init()

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)


def maximize_console(lines=None):
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    h_wnd = kernel32.GetConsoleWindow()
    if cols and h_wnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 9999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
            cols, lines))
        user32.ShowWindow(h_wnd, SW_MAXIMIZE)

    return max_size.X, max_size.Y


x, y = maximize_console()

running = True
chars = 'abcdefghijklmnopqrstuvwxyz#1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        return False  # stop listener


listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

while running:
    print(f'{Fore.GREEN}', end='')

    for i in range(int(x)):
        print(random.choice(chars), end='')

    print(f'{Style.RESET_ALL}')
    sleep(0.0019)

listener.join()
