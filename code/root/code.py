import board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep, monotonic
import fonctions_touches

# Définition des entrées
btns = []
for i in range(6):
    btn = DigitalInOut(getattr(board, f"GP{i}"))
    btn.direction = Direction.INPUT
    btn.pull = Pull.UP
    btns.append(btn)

def litTouche(): # retourne la valeur de la touche appuyée (255 en cas d'échec)
    looptime = monotonic()
    while (monotonic() - looptime) < 1: # attente résultat lecture touche 1 seconde
        for i in range(6):
            if btns[i].value == False:
                return i
    return 255

def liberationTouche(): # attend que toutes les touches soient relâchées  
    while not all(btn.value for btn in btns):
        pass

print('Up and running.')
while True:# ------------------------MAIN LOOP--------------------------------------------------------

    # attente détection touche
    while all(btn.value for btn in btns):
        pass

    numTouche = litTouche() # numéro de la touche    
    start = monotonic() # mesure ds temps d'appui
    sleep(0.1) # pause ms pour debounce touche (évite faux double clicks)
    liberationTouche() # attente relachement touche

    click = 1 if (monotonic() - start) < 0.3 else 3 # détection appui court ou long
     
    while (monotonic() - start) < 0.3: # détection double click
        if not all(btn.value for btn in btns):
            if numTouche == litTouche(): # si c'est la même touche
                click = 2
                sleep(0.1) # temps en ms pour debounce touche
                liberationTouche()
    print ('touche :',numTouche,' click :',click)
 
    if click == 1: # appui court
        getattr(fonctions_touches, f"court{numTouche}")()
        
    if click == 2: # double click       
        getattr(fonctions_touches, f"double{numTouche}")()
            
    if click == 3: # appui long
        getattr(fonctions_touches, f"long{numTouche}")()
 
    click=0
    numTouche=255
# ------------------------MAIN LOOP--------------------------------------------------------