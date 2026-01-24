# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
# SPDX-FileCopyrightText: 2025 Amélioration FR avec accents et AltGr
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.keyboard_layout_fr.KeyboardLayoutFR`
=======================================================

Layout clavier AZERTY français complet avec support :
- Tous les caractères ASCII
- Accents français (é, è, à, ù, ç, ê, etc.)
- Caractères AltGr (#, @, [, ], {, }, |, ~, etc.)
- Optimisation des release

Auteur(s): Dan Halbert (base), Adaptation FR améliorée
"""

from .keycode import Keycode


class KeyboardLayoutFR:
    """Map ASCII et caractères français étendus vers frappes clavier AZERTY.
    
    Support complet des accents français et caractères spéciaux.
    """

    # Flags pour modificateurs
    SHIFT_FLAG = 0x80
    ALTGR_FLAG = 0x40
    
    # Table ASCII de base (0-127)
    ASCII_TO_KEYCODE = (
        b"\x00"  # NUL
        b"\x00"  # SOH
        b"\x00"  # STX
        b"\x00"  # ETX
        b"\x00"  # EOT
        b"\x00"  # ENQ
        b"\x00"  # ACK
        b"\x00"  # BEL
        b"\x2a"  # BS (Backspace)
        b"\x2b"  # TAB
        b"\x28"  # LF (Enter)
        b"\x00"  # VT
        b"\x00"  # FF
        b"\x28"  # CR (Enter)
        b"\x00"  # SO
        b"\x00"  # SI
        b"\x00"  # DLE
        b"\x00"  # DC1
        b"\x00"  # DC2
        b"\x00"  # DC3
        b"\x00"  # DC4
        b"\x00"  # NAK
        b"\x00"  # SYN
        b"\x00"  # ETB
        b"\x00"  # CAN
        b"\x00"  # EM
        b"\x00"  # SUB
        b"\x29"  # ESC
        b"\x00"  # FS
        b"\x00"  # GS
        b"\x00"  # RS
        b"\x00"  # US
        b"\x2c"  # SPACE
        b"\x38"  # !
        b"\x20"  # "
        b"\x70"  # # (AltGr + 3) - encodé avec ALTGR_FLAG
        b"\x30"  # $
        b"\xb4"  # %
        b"\x1e"  # &
        b"\x21"  # '
        b"\x22"  # (
        b"\x2d"  # )
        b"\x31"  # *
        b"\xae"  # +
        b"\x10"  # ,
        b"\x23"  # -
        b"\xb6"  # .
        b"\xb7"  # /
        b"\xa7"  # 0
        b"\x9e"  # 1
        b"\x9f"  # 2
        b"\xa0"  # 3
        b"\xa1"  # 4
        b"\xa2"  # 5
        b"\xa3"  # 6
        b"\xa4"  # 7
        b"\xa5"  # 8
        b"\xa6"  # 9
        b"\x37"  # :
        b"\x36"  # ;
        b"\x64"  # <
        b"\x2e"  # =
        b"\xe4"  # >
        b"\x90"  # ?
        b"\x67"  # @ (AltGr + à) - encodé avec ALTGR_FLAG
        b"\x94"  # A
        b"\x85"  # B
        b"\x86"  # C
        b"\x87"  # D
        b"\x88"  # E
        b"\x89"  # F
        b"\x8a"  # G
        b"\x8b"  # H
        b"\x8c"  # I
        b"\x8d"  # J
        b"\x8e"  # K
        b"\x8f"  # L
        b"\xb3"  # M
        b"\x91"  # N
        b"\x92"  # O
        b"\x93"  # P
        b"\x84"  # Q
        b"\x95"  # R
        b"\x96"  # S
        b"\x97"  # T
        b"\x98"  # U
        b"\x99"  # V
        b"\x9d"  # W
        b"\x9b"  # X
        b"\x9c"  # Y
        b"\x9a"  # Z
        b"\x62"  # [ (AltGr + 5)
        b"\x25"  # \ (AltGr + 8)
        b"\x2d"  # ] (AltGr + -)
        b"\x2f"  # ^
        b"\x25"  # _
        b"\x24"  # ` (AltGr + è)
        b"\x14"  # a
        b"\x05"  # b
        b"\x06"  # c
        b"\x07"  # d
        b"\x08"  # e
        b"\x09"  # f
        b"\x0a"  # g
        b"\x0b"  # h
        b"\x0c"  # i
        b"\x0d"  # j
        b"\x0e"  # k
        b"\x0f"  # l
        b"\x33"  # m
        b"\x11"  # n
        b"\x12"  # o
        b"\x13"  # p
        b"\x04"  # q
        b"\x15"  # r
        b"\x16"  # s
        b"\x17"  # t
        b"\x18"  # u
        b"\x19"  # v
        b"\x1d"  # w
        b"\x1b"  # x
        b"\x1c"  # y
        b"\x1a"  # z
        b"\x61"  # { (AltGr + 4)
        b"\x23"  # | (AltGr + 6)
        b"\x2e"  # } (AltGr + =)
        b"\x9f"  # ~ (AltGr + 2)
        b"\x4c"  # DEL
    )

    # Table étendue pour caractères français (Latin-1 étendu)
    # Format: 'caractère': (modificateurs, keycode)
    EXTENDED_CHARS = {
        # Lettres accentuées minuscules
        'à': (0, 0x14),      # à (touche directe)
        'â': (0x2f, 0x14),   # ^ puis a (dead key)
        'é': (0, 0x9f),      # é (touche 2)
        'è': (0, 0x24),      # è (touche 7)
        'ê': (0x2f, 0x08),   # ^ puis e
        'ë': (0, 0x00),      # Non disponible directement
        'î': (0x2f, 0x0c),   # ^ puis i
        'ï': (0, 0x00),      # Non disponible directement
        'ô': (0x2f, 0x12),   # ^ puis o
        'ù': (0, 0x34),      # ù (touche directe)
        'û': (0x2f, 0x18),   # ^ puis u
        'ü': (0, 0x00),      # Non disponible directement
        'ç': (0, 0x26),      # ç (touche 9)
        'œ': (0, 0x00),      # Non disponible
        'æ': (0, 0x00),      # Non disponible
        
        # Lettres accentuées majuscules
        'À': (SHIFT_FLAG, 0x14),
        'Â': (0x2f, 0x94),   # ^ puis A
        'É': (SHIFT_FLAG, 0x9f),
        'È': (SHIFT_FLAG, 0x24),
        'Ê': (0x2f, 0x88),   # ^ puis E
        'Î': (0x2f, 0x8c),   # ^ puis I
        'Ô': (0x2f, 0x92),   # ^ puis O
        'Ù': (SHIFT_FLAG, 0x34),
        'Û': (0x2f, 0x98),   # ^ puis U
        'Ç': (SHIFT_FLAG, 0x26),
        
        # Caractères spéciaux européens
        '€': (ALTGR_FLAG, 0x08),  # AltGr + e
        '£': (ALTGR_FLAG, 0x30),  # AltGr + $
        '¤': (0, 0x00),           # Non disponible
        
        # Guillemets français
        '«': (0, 0x00),  # Non standard sur AZERTY
        '»': (0, 0x00),  # Non standard sur AZERTY
    }

    def __init__(self, keyboard):
        """Initialise le layout pour le clavier donné.

        :param keyboard: Un objet Keyboard. Les caractères seront envoyés à ce clavier.

        Example::

            from adafruit_hid.keyboard import Keyboard
            import usb_hid
            
            kbd = Keyboard(usb_hid.devices)
            layout = KeyboardLayoutFR(kbd)
        """
        self.keyboard = keyboard

    def write(self, string):
        """Tape la chaîne en pressant et relâchant les touches.

        :param string: Une chaîne de caractères ASCII ou français étendus.
        :raises ValueError: si un caractère n'a pas de keycode disponible.

        Example::

            # Écrit "Bonjour !" suivi d'Enter
            layout.write('Bonjour !\\n')
            
            # Écrit avec accents
            layout.write('Voilà une chaîne accentuée')
        """
        for char in string:
            self._press_char(char)

    def _press_char(self, char):
        """Presse et relâche les touches nécessaires pour un caractère."""
        # Vérifier d'abord dans la table étendue
        if char in self.EXTENDED_CHARS:
            modifier, keycode = self.EXTENDED_CHARS[char]
            
            # Cas spécial: dead keys (^ pour accents circonflexes)
            if modifier == 0x2f:  # Dead key ^
                self.keyboard.press(modifier)
                self.keyboard.release_all()
                self.keyboard.press(keycode)
                self.keyboard.release_all()
            elif keycode == 0:
                raise ValueError(f"Caractère '{char}' non disponible sur clavier FR AZERTY")
            else:
                if modifier & self.SHIFT_FLAG:
                    self.keyboard.press(Keycode.SHIFT)
                if modifier & self.ALTGR_FLAG:
                    self.keyboard.press(Keycode.RIGHT_ALT)  # AltGr
                self.keyboard.press(keycode)
                self.keyboard.release_all()
        else:
            # Utiliser la table ASCII standard
            keycode = self._char_to_keycode(char)
            
            # Gérer SHIFT
            if keycode & self.SHIFT_FLAG:
                keycode &= ~self.SHIFT_FLAG
                self.keyboard.press(Keycode.SHIFT)
            
            # Gérer AltGr
            if keycode & self.ALTGR_FLAG:
                keycode &= ~self.ALTGR_FLAG
                self.keyboard.press(Keycode.RIGHT_ALT)
            
            self.keyboard.press(keycode)
            self.keyboard.release_all()

    def keycodes(self, char):
        """Retourne le tuple de keycodes nécessaires pour taper un caractère.

        :param char: Un caractère unique.
        :type char: str de longueur 1
        :returns: tuple de keycodes Keycode
        :raises ValueError: si le caractère n'a pas de keycode disponible

        Examples::

            # Retourne (Keycode.TAB,)
            keycodes('\\t')
            
            # Retourne (Keycode.A,)
            keycodes('a')
            
            # Retourne (Keycode.SHIFT, Keycode.A)
            keycodes('A')
            
            # Retourne les keycodes pour é
            keycodes('é')
        """
        # Vérifier table étendue d'abord
        if char in self.EXTENDED_CHARS:
            modifier, keycode = self.EXTENDED_CHARS[char]
            if keycode == 0:
                raise ValueError(f"Caractère '{char}' non disponible")
            
            result = []
            if modifier & self.SHIFT_FLAG:
                result.append(Keycode.SHIFT)
            if modifier & self.ALTGR_FLAG:
                result.append(Keycode.RIGHT_ALT)
            result.append(keycode)
            return tuple(result)
        
        # Table ASCII standard
        keycode = self._char_to_keycode(char)
        result = []
        
        if keycode & self.SHIFT_FLAG:
            result.append(Keycode.SHIFT)
            keycode &= ~self.SHIFT_FLAG
        
        if keycode & self.ALTGR_FLAG:
            result.append(Keycode.RIGHT_ALT)
            keycode &= ~self.ALTGR_FLAG
        
        result.append(keycode)
        return tuple(result)

    def _char_to_keycode(self, char):
        """Retourne le keycode HID pour un caractère ASCII.
        
        Les flags SHIFT_FLAG et ALTGR_FLAG peuvent être activés.
        Vous devez les masquer avant d'envoyer le keycode dans un rapport USB.
        """
        char_val = ord(char)
        if char_val > 127:
            raise ValueError(
                f"Caractère '{char}' (U+{char_val:04X}) hors de la table ASCII. "
                f"Utilisez la table EXTENDED_CHARS pour les accents français."
            )
        
        keycode = self.ASCII_TO_KEYCODE[char_val]
        if keycode == 0:
            raise ValueError(f"Pas de keycode disponible pour le caractère '{char}'")
        
        return keycode
