"""
Clavier Macro 6 Touches - Raspberry Pi Pico
============================================
Auteur: Hugues Goussard
Version: 3.0 (avec configuration TOML)

Supporte:
- Appui court
- Appui long (> 0.3s)
- Double-clic
- Configuration via config.toml
- Profils multiples
"""

import board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep, monotonic
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_fr import KeyboardLayoutFR

from config_manager import ConfigManager

# ==================== CHARGEMENT CONFIGURATION ====================

config = ConfigManager()

# Créer un fichier de config par défaut si inexistant
# Décommenter cette ligne au premier lancement:
# config.create_default_config()

# ==================== INITIALISATION HID ====================

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutFR(keyboard)

# ==================== PARAMÈTRES (depuis config.toml) ====================

DEBOUNCE_TIME = config.get('settings', 'debounce', default=0.1)
LONG_PRESS_THRESHOLD = config.get('settings', 'long_press', default=0.3)
DOUBLE_CLICK_WINDOW = config.get('settings', 'double_click_window', default=0.3)
READ_TIMEOUT = 1.0

USERNAME = config.get('user', 'username', default='')
SSH_USER = config.get('user', 'ssh_user', default='')
SSH_HOST = config.get('user', 'ssh_host', default='')
TERMINAL_DELAY = config.get('user', 'terminal_delay', default=0.5)

NO_BUTTON = 255
CLICK_SHORT = 1
CLICK_DOUBLE = 2
CLICK_LONG = 3

# ==================== INITIALISATION BOUTONS ====================

BUTTON_PINS = [
    board.GP0,  # Bouton 0
    board.GP1,  # Bouton 1
    board.GP2,  # Bouton 2
    board.GP3,  # Bouton 3
    board.GP4,  # Bouton 4
    board.GP5,  # Bouton 5
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
    """Retourne l'index du premier bouton pressé"""
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


# ==================== EXÉCUTION DES ACTIONS ====================

def execute_keycombo(combo_string):
    """Exécute un raccourci clavier depuis une string
    
    Args:
        combo_string: "CTRL+C", "CTRL+SHIFT+V", etc.
    """
    keycodes = config.parse_keycombo(combo_string)
    if keycodes:
        keyboard.send(*keycodes)
    else:
        print(f'⚠ Combo invalide: {combo_string}')


def execute_text(text):
    """Tape du texte
    
    Args:
        text: Texte à taper (supporte \\n pour Enter)
    """
    # Remplacer les \\n par de vrais retours à la ligne
    text = text.replace('\\n', '\n')
    keyboard_layout.write(text)


def execute_command(command_type):
    """Exécute une commande spéciale
    
    Args:
        command_type: Type de commande ('ssh', etc.)
    """
    if command_type == 'ssh':
        # Ouvrir terminal + SSH
        keyboard.send(config.KEYCODE_MAP['CTRL'], 
                     config.KEYCODE_MAP['ALT'], 
                     config.KEYCODE_MAP['T'])
        sleep(TERMINAL_DELAY)
        
        if SSH_HOST:
            ssh_command = f'ssh -o StrictHostKeyChecking=no {SSH_USER}@{SSH_HOST}'
        else:
            ssh_command = f'ssh -o StrictHostKeyChecking=no {SSH_USER}@'
        
        keyboard_layout.write(ssh_command)
        
        # Si pas d'hôte, coller depuis presse-papier
        if not SSH_HOST:
            keyboard.send(config.KEYCODE_MAP['CTRL'],
                         config.KEYCODE_MAP['SHIFT'],
                         config.KEYCODE_MAP['V'])
    else:
        print(f'⚠ Commande inconnue: {command_type}')


def execute_action(button_num, click_type):
    """Exécute l'action appropriée selon le bouton et le type de clic
    
    Args:
        button_num: Numéro du bouton (0-5)
        click_type: CLICK_SHORT, CLICK_DOUBLE ou CLICK_LONG
    """
    if button_num == NO_BUTTON:
        return
    
    # Mapper click_type vers string
    click_names = {
        CLICK_SHORT: 'short',
        CLICK_DOUBLE: 'double',
        CLICK_LONG: 'long'
    }
    click_str = click_names.get(click_type, 'short')
    
    # Récupérer l'action depuis la config
    action_config = config.get_button_action(button_num, click_str)
    
    if not action_config:
        print(f'⚠ Aucune action: bouton {button_num} - {click_str}')
        return
    
    action_type = action_config.get('type', 'keycombo')
    action = action_config.get('action', '')
    
    try:
        if action_type == 'keycombo':
            execute_keycombo(action)
        elif action_type == 'text':
            execute_text(action)
        elif action_type == 'command':
            execute_command(action)
        else:
            print(f'⚠ Type d\'action inconnu: {action_type}')
    except Exception as e:
        print(f'✗ Erreur action bouton {button_num}: {e}')


def detect_click_type(button_num, press_start_time):
    """Détecte le type de clic (court, long ou double)"""
    sleep(DEBOUNCE_TIME)
    wait_for_release()
    press_duration = monotonic() - press_start_time
    
    if press_duration >= LONG_PRESS_THRESHOLD:
        return CLICK_LONG
    
    double_click_deadline = monotonic() + DOUBLE_CLICK_WINDOW
    
    while monotonic() < double_click_deadline:
        if not all_buttons_released():
            second_button = get_pressed_button(timeout=0.1)
            if second_button == button_num:
                sleep(DEBOUNCE_TIME)
                wait_for_release()
                return CLICK_DOUBLE
    
    return CLICK_SHORT


# ==================== GESTION DES PROFILS ====================

def cycle_profile():
    """Change de profil (cycle à travers tous les profils)"""
    profiles = config.list_profiles()
    if len(profiles) <= 1:
        print('Un seul profil disponible')
        return
    
    current = config.config.get('current_profile', 'default')
    try:
        current_idx = profiles.index(current)
        next_idx = (current_idx + 1) % len(profiles)
        next_profile = profiles[next_idx]
        config.switch_profile(next_profile)
        
        # Feedback visuel (si LED disponible)
        # Blink LED ou afficher sur OLED
        
    except ValueError:
        # Profil actuel n'existe plus, prendre le premier
        config.switch_profile(profiles[0])


# ==================== BOUCLE PRINCIPALE ====================

print('=' * 50)
print('Clavier Macro - Version 3.0 avec Config TOML')
print('=' * 50)
print(f'Profil actif: {config.config.get("current_profile", "default")}')
print(f'Profils disponibles: {", ".join(config.list_profiles())}')
print(f'Debounce: {DEBOUNCE_TIME}s | Long press: {LONG_PRESS_THRESHOLD}s')
print('Prêt à l\'emploi')
print('=' * 50)

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
    
    # Afficher l'action qui va être exécutée
    action_config = config.get_button_action(
        button_pressed, 
        click_names[click_type]
    )
    if action_config:
        desc = action_config.get('description', 'N/A')
        print(f'[{config.config["current_profile"]}] Bouton {button_pressed} - {click_names[click_type]}: {desc}')
    
    # Exécuter l'action
    execute_action(button_pressed, click_type)
    
    # Petit délai avant la prochaine lecture
    sleep(0.05)