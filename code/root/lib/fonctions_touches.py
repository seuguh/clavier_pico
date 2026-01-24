"""fonctions_touches.py
====================================================
* Author(s): Hugues Goussard

Fonctions exécutées lors des appuis sur les touches du clavier macro.

Numérotation des touches:
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

Nomenclature des fonctions:
- short0()  -> appui court touche 0
- long0()   -> appui long touche 0
- short1()  -> appui court touche 1
- long1()   -> appui long touche 1
etc...
"""

import usb_hid
from adafruit_hid.keyboard import Keyboard, Keycode
from adafruit_hid.keyboard_layout_fr import KeyboardLayoutFR
from time import sleep

# Configuration globale
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutFR(keyboard)

# ============ CONFIGURATION UTILISATEUR ============
# Modifiez ces constantes selon vos besoins

USERNAME = 'hgoussard01'
SSH_USER = 'hugues.goussard'
SSH_HOST = ''  # À compléter avec l'adresse du serveur

TERMINAL_OPEN_DELAY = 0.5  # secondes d'attente pour l'ouverture du terminal

# ===================================================


# ========== TOUCHE 0 : COPIER ==========

def short0():
    """Copier (Ctrl+C)"""
    keyboard.send(Keycode.CONTROL, Keycode.C)


def long0():
    """Copier avec formatage (Ctrl+Shift+C) - utile dans terminaux"""
    keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.C)


# ========== TOUCHE 1 : COLLER ==========

def short1():
    """Coller (Ctrl+V)"""
    keyboard.send(Keycode.CONTROL, Keycode.V)


def long1():
    """Coller sans formatage (Ctrl+Shift+V) - utile dans terminaux"""
    keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.V)


# ========== TOUCHE 2 : COUPER ==========

def short2():
    """Couper (Ctrl+X)"""
    keyboard.send(Keycode.CONTROL, Keycode.X)


def long2():
    """Supprimer ligne entière (Ctrl+Shift+K) - VSCode/Sublime"""
    keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.K)


# ========== TOUCHE 3 : ANNULER ==========

def short3():
    """Annuler (Ctrl+Z)"""
    keyboard.send(Keycode.CONTROL, Keycode.Z)


def long3():
    """Refaire (Ctrl+Y ou Ctrl+Shift+Z)"""
    keyboard.send(Keycode.CONTROL, Keycode.Y)


# ========== TOUCHE 4 : CREDENTIALS / SSH ==========

def short4():
    """Tape le nom d'utilisateur"""
    keyboard_layout.write(USERNAME)


def long4():
    """Ouvre un terminal et lance SSH"""
    # Ouvrir un nouveau terminal (Ctrl+Alt+T sur Ubuntu/Debian)
    keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.T)
    sleep(TERMINAL_OPEN_DELAY)
    
    # Commande SSH complète avec @ qui fonctionne maintenant !
    if SSH_HOST:
        ssh_command = f'ssh -o StrictHostKeyChecking=no {SSH_USER}@{SSH_HOST}'
    else:
        # Si pas d'hôte configuré, juste le début de la commande
        ssh_command = f'ssh -o StrictHostKeyChecking=no {SSH_USER}@'
    
    keyboard_layout.write(ssh_command)
    
    # Si pas d'hôte, coller depuis le presse-papier
    if not SSH_HOST:
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.V)


# ========== TOUCHE 5 : FONCTIONS DIVERSES ==========

def short5():
    """Rechercher (Ctrl+F)"""
    keyboard.send(Keycode.CONTROL, Keycode.F)


def long5():
    """Rechercher et remplacer (Ctrl+H)"""
    keyboard.send(Keycode.CONTROL, Keycode.H)


# ========== FONCTIONS UTILITAIRES ==========

def send_keycombo(*keycodes):
    """Envoie une combinaison de touches de manière sûre"""
    keyboard.send(*keycodes)


def type_and_enter(text):
    """Tape du texte et appuie sur Entrée"""
    keyboard_layout.write(text)
    keyboard.send(Keycode.ENTER)


def clear_line():
    """Efface la ligne courante dans un terminal"""
    keyboard.send(Keycode.CONTROL, Keycode.U)


# ========== EXEMPLES DE FONCTIONS AVANCÉES (commentées) ==========

# def short4_alternative():
#     """Alternative: tape email complet"""
#     keyboard_layout.write(f'{SSH_USER}@example.com')

# def long4_alternative():
#     """Alternative: lance une connexion SCP"""
#     keyboard_layout.write(f'scp fichier.txt {SSH_USER}@{SSH_HOST}:~/')

# def short5_snippets():
#     """Exemple: insère des snippets de code Python"""
#     keyboard_layout.write('#!/usr/bin/env python3\n')
#     keyboard_layout.write('# -*- coding: utf-8 -*-\n\n')

# def long5_git_commit():
#     """Exemple: séquence Git commit"""
#     type_and_enter('git add .')
#     sleep(0.2)
#     keyboard_layout.write('git commit -m ""')
#     keyboard.send(Keycode.LEFT_ARROW)  # Se positionner entre les guillemets
