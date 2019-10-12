import time
import win32api,win32gui,win32con
from ctypes import *

def clickLeftCur():
   win32api.mouse_event(
    win32con.MOUSEEVENTF_LEFTDOWN|
   win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def moveCurPos(x,y):
    windll.user32.SetCursorPos(x, y)

def click_left(x, y):
    moveCurPos(x, y)
    clickLeftCur()

# def down_move_to(x, y):
    # pyautogui.mouseDown(x=x, y=y, button='left')
    # pyautogui.moveTo(x, y)

x = time.time()
click_left(1,1)
click_left(10,10)
click_left(100,100)
click_left(1000,1000)
y = time.time()
print(y-x)