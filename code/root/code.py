import board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep, monotonic
import fonctions_touches

#Définition des entrées
btn0 = DigitalInOut(board.GP0)
btn0.direction = Direction.INPUT
btn0.pull = Pull.UP
btn1 = DigitalInOut(board.GP1)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP
btn2 = DigitalInOut(board.GP2)
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP
btn3 = DigitalInOut(board.GP3)
btn3.direction = Direction.INPUT
btn3.pull = Pull.UP
btn4 = DigitalInOut(board.GP4)
btn4.direction = Direction.INPUT
btn4.pull = Pull.UP
btn5 = DigitalInOut(board.GP5)
btn5.direction = Direction.INPUT
btn5.pull = Pull.UP


def litTouche(): # retourne la valeur de la touche appuyée (255 en cas d'échec)

 looptime = monotonic()
 while (monotonic() - looptime) < 1: # attente résultat lecture touche 1 seconde
     if btn0.value == False:
        return 0
     if btn1.value  == False:
        return 1
     if btn2.value == False:
        return 2
     if btn3.value == False:
        return 3
     if btn4.value == False:
        return 4
     if btn5.value == False:
        return 5
 return 255

def liberationTouche(): # attend que toutes les touches soient relâchées  
 while not(btn0.value and btn1.value and btn2.value and btn3.value and btn4.value and btn5.value):
   pass

print('Up and running.')
while True:# ------------------------MAIN LOOP--------------------------------------------------------

 # attente détection touche
 while (btn0.value and btn1.value and btn2.value and btn3.value and btn4.value and btn5.value):
   pass

 numTouche = litTouche() # numéro de la touche    
 start = monotonic() # mesure ds temps d'appui
 sleep(0.1) # pause ms pour debounce touche (évite faux double clicks)
 liberationTouche() # attente relachement touche

 click = 1 if (monotonic() - start) < 0.3 else 3 # détection appui court ou long
     
 while (monotonic() - start) < 0.3: # détection double click
   if not(btn0.value and btn1.value and btn2.value and btn3.value and btn4.value and btn5.value):
       if numTouche == litTouche(): # si c'est la même touche
           click = 2
           sleep(0.1) # temps en ms pour debounce touche
           liberationTouche()
 print ('touche :',numTouche,' click :',click)
 if click == 1: # appui court
    if numTouche == 0: # touche copier
        fonctions_touches.court0()
    if numTouche == 1: # touche coller
        fonctions_touches.court1()   
    if numTouche == 2: # touche couper
        fonctions_touches.court2()
    if numTouche == 3: # touche annuler   
        fonctions_touches.court3()      
    if numTouche == 4: # touche ID/SSH
        fonctions_touches.court4() 
    if numTouche == 5: # touche Anim. ON/OFF   
        fonctions_touches.court5()
        
 if click == 2: # double click       
    if numTouche == 0: # touche copier
        fonctions_touches.double0()
    if numTouche == 1: # touche coller
        fonctions_touches.double1()   
    if numTouche == 2: # touche couper
        fonctions_touches.double2()
    if numTouche == 3: # touche annuler   
        fonctions_touches.double3()      
    if numTouche == 4: # touche ID/SSH
        fonctions_touches.double4() 
    if numTouche == 5: # touche Anim. ON/OFF   
        fonctions_touches.double5()       
            
 if click == 3: # appui long
    if numTouche == 0: # touche copier
        fonctions_touches.long0()
    if numTouche == 1: # touche coller        
        fonctions_touches.long1()
    if numTouche == 2: # touche couper        
        fonctions_touches.long2()
    if numTouche == 3: # touche annuler         
        fonctions_touches.long3() 
    if numTouche == 4: # touche ID/SSH        
        fonctions_touches.long4()
    if numTouche == 5: # touche Anim. ON/OFF        
        fonctions_touches.long5()  
 
 click=0
 numTouche=255
# ------------------------MAIN LOOP--------------------------------------------------------
