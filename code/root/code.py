"""
Clavier Macro 6 Touches - Raspberry Pi Pico
============================================
Auteur: Hugues Goussard
Version: 2.0 (refactorisée)

Supporte:
- Appui court
- Appui long (> 0.3s)
- Double-clic
"""

import board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep, monotonic
import fonctions_touches

# ==================== CONFIGURATION ====================

DEBOUNCE_TIME = 0.1          # Temps anti-rebond (secondes)
LONG_PRESS_THRESHOLD = 0.3   # Seuil appui court/long (secondes)
DOUBLE_CLICK_WINDOW = 0.3    # Fenêtre détection double-clic (secondes)
READ_TIMEOUT = 1.0           # Timeout lecture touche (secondes)

NO_BUTTON = 255              # Valeur indiquant aucune touche
CLICK_SHORT = 1
CLICK_DOUBLE = 2
CLICK_LONG = 3

# ==================== INITIALISATION BOUTONS ====================

BUTTON_PINS = [
    board.GP0,  # Bouton 0 - Copier
    board.GP1,  # Bouton 1 - Coller
    board.GP2,  # Bouton 2 - Couper
    board.GP3,  # Bouton 3 - Annuler
    board.GP4,  # Bouton 4 - ID/SSH
    board.GP5,  # Bouton 5 - Recherche
]

buttons = []
for pin in BUTTON_PINS:
    btn = DigitalInOut(pin)
    btn.direction = Direction.INPUT
    btn.pull = Pull.UP
    buttons.append(btn)

# ==================== FONCTIONS UTILITAIRES ====================

def all_buttons_released():
    """Retourne True si tous les boutons sont relâchés"""
    return all(btn.value for btn in buttons)


def wait_for_any_press():
    """Attend qu'un bouton soit pressé"""
    while all_buttons_released():
        pass


def get_pressed_button(timeout=READ_TIMEOUT):
    """Retourne l'index du premier bouton pressé.
    
    Args:
        timeout: Temps maximum d'attente en secondes
        
    Returns:
        Index du bouton (0-5) ou NO_BUTTON si timeout
    """
    start_time = monotonic()
    while (monotonic() - start_time) < timeout:
        for i, btn in enumerate(buttons):
            if not btn.value:
                return i
    return NO_BUTTON


def wait_for_release():
    """Attend que tous les boutons soient relâchés"""
    while not all_buttons_released():
        pass


def execute_action(button_num, click_type):
    """Exécute l'action appropriée selon le bouton et le type de clic.
    
    Args:
        button_num: Numéro du bouton (0-5)
        click_type: CLICK_SHORT, CLICK_DOUBLE ou CLICK_LONG
    """
    if button_num == NO_BUTTON:
        return
    
    # Mapping des fonctions
    actions = {
        0: {  # Bouton 0 - Copier
            CLICK_SHORT: fonctions_touches.short0,
            CLICK_DOUBLE: fonctions_touches.double0 if hasattr(fonctions_touches, 'double0') else None,
            CLICK_LONG: fonctions_touches.long0,
        },
        1: {  # Bouton 1 - Coller
            CLICK_SHORT: fonctions_touches.short1,
            CLICK_DOUBLE: fonctions_touches.double1 if hasattr(fonctions_touches, 'double1') else None,
            CLICK_LONG: fonctions_touches.long1,
        },
        2: {  # Bouton 2 - Couper
            CLICK_SHORT: fonctions_touches.short2,
            CLICK_DOUBLE: fonctions_touches.double2 if hasattr(fonctions_touches, 'double2') else None,
            CLICK_LONG: fonctions_touches.long2,
        },
        3: {  # Bouton 3 - Annuler
            CLICK_SHORT: fonctions_touches.short3,
            CLICK_DOUBLE: fonctions_touches.double3 if hasattr(fonctions_touches, 'double3') else None,
            CLICK_LONG: fonctions_touches.long3,
        },
        4: {  # Bouton 4 - ID/SSH
            CLICK_SHORT: fonctions_touches.short4,
            CLICK_DOUBLE: fonctions_touches.double4 if hasattr(fonctions_touches, 'double4') else None,
            CLICK_LONG: fonctions_touches.long4,
        },
        5: {  # Bouton 5 - Recherche
            CLICK_SHORT: fonctions_touches.short5,
            CLICK_DOUBLE: fonctions_touches.double5 if hasattr(fonctions_touches, 'double5') else None,
            CLICK_LONG: fonctions_touches.long5,
        },
    }
    
    # Exécuter l'action si elle existe
    if button_num in actions and click_type in actions[button_num]:
        action = actions[button_num][click_type]
        if action is not None:
            try:
                action()
            except Exception as e:
                print(f'Erreur fonction bouton {button_num}, click {click_type}: {e}')
        else:
            print(f'Action non définie: bouton {button_num}, click {click_type}')


def detect_click_type(button_num, press_start_time):
    """Détecte le type de clic (court, long ou double).
    
    Args:
        button_num: Numéro du bouton pressé
        press_start_time: Timestamp du début de l'appui
        
    Returns:
        CLICK_SHORT, CLICK_DOUBLE ou CLICK_LONG
    """
    # Debounce
    sleep(DEBOUNCE_TIME)
    
    # Attendre le relâchement
    wait_for_release()
    press_duration = monotonic() - press_start_time
    
    # Déterminer si appui court ou long
    if press_duration >= LONG_PRESS_THRESHOLD:
        return CLICK_LONG
    
    # Fenêtre de détection double-clic
    double_click_deadline = monotonic() + DOUBLE_CLICK_WINDOW
    
    while monotonic() < double_click_deadline:
        if not all_buttons_released():
            second_button = get_pressed_button(timeout=0.1)
            if second_button == button_num:
                # C'est un double-clic !
                sleep(DEBOUNCE_TIME)
                wait_for_release()
                return CLICK_DOUBLE
    
    # Pas de deuxième clic détecté
    return CLICK_SHORT


# ==================== BOUCLE PRINCIPALE ====================

print('Clavier macro démarré - Prêt à l\'emploi')

while True:
    # Attendre qu'un bouton soit pressé
    wait_for_any_press()
    
    # Identifier quel bouton et quand
    press_start = monotonic()
    button_pressed = get_pressed_button(timeout=0.1)
    
    if button_pressed == NO_BUTTON:
        continue
    
    # Déterminer le type de clic
    click_type = detect_click_type(button_pressed, press_start)
    
    # Afficher pour debug
    click_names = {
        CLICK_SHORT: 'court',
        CLICK_DOUBLE: 'double',
        CLICK_LONG: 'long'
    }
    print(f'Bouton {button_pressed} - {click_names.get(click_type, "inconnu")}')
    
    # Exécuter l'action
    execute_action(button_pressed, click_type)
    
    # Petit délai avant la prochaine lecture
    sleep(0.05)
