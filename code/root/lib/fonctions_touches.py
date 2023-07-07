"""fonctions_touches.py
====================================================
* Author(s): Hugues Goussard

Fonctions qui seront exécutées lors des appuis sur les touches.

Numérotation des touches

    USB
     ^
+---+ +---+ 
| 4 | | 5 | 
+---+ +---+ 
+---+ +---+ 
| 2 | | 3 | 
+---+ +---+ 
+---+ +---+ 
| 0 | | 1 | 
+---+ +---+ 

nom des fonctions:

long0()    -> appui long touche 0
court0()   -> appui court touche 0
double0()  -> double click touche 0
long1()    -> appui long touche 1
court1()   -> appui court touche 1
double1()  -> double click touche 1
etc...


"""

import usb_hid
from adafruit_hid.keyboard import Keyboard, Keycode
from adafruit_hid.keyboard_layout_fr import KeyboardLayoutFR
from time import sleep
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutFR(keyboard)


# Fonctions --------------------------------------------
def court0():
  keyboard.send(Keycode.CONTROL,Keycode.C)
def long0():
  keyboard.send(Keycode.SHIFT,Keycode.CONTROL,Keycode.C)
def double0():
  pass

def court1():
  keyboard.send(Keycode.CONTROL,Keycode.V)
def long1():
  keyboard.send(Keycode.CONTROL,Keycode.SHIFT,Keycode.V)
def double1():
  pass

def court2():
  keyboard.send(Keycode.CONTROL,Keycode.X)
def long2():
  pass
def double2():
  pass

def court3():
  keyboard.send(Keycode.CONTROL,Keycode.Z)
def long3():
  pass
def double3():
  pass

def court4():
    keyboard_layout.write('hgoussard01')
def long4():
    # ouvre un terminal  
    keyboard.send(Keycode.CONTROL,Keycode.ALT,Keycode.T)
    time.sleep(0.5) # temps d'ouverture du terminal
    keyboard_layout.write('ssh -o StrictHostKeyChecking=no hugues.goussard') # l'@ n'est pas encore gérable ici
    keyboard.send(Keycode.RIGHT_ALT,Keycode.ZERO) # code pour @
    keyboard.send(Keycode.CONTROL,Keycode.SHIFT,Keycode.V)
def double4():
  pass

def court5():
  pass
def long5():
  pass
def double5():
  pass

