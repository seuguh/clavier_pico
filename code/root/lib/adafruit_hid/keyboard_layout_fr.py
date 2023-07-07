# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.keyboard_layout_ff.KeyboardLayoutFR`
=======================================================

* DERIVATIVE FROM keyboard_layout_US Author(s): Dan Halbert

Adaptation pour gérer les touches FR. y'a pas tout mais presque. :)
"""

from .keycode import Keycode


class KeyboardLayoutFR:
    """Map ASCII characters to appropriate keypresses on a standard FR PC keyboard.

    Non-ASCII characters and most control characters will raise an exception.
    """

    # The ASCII_TO_KEYCODE bytes object is used as a table to maps ASCII 0-127
    # to the corresponding # keycode on a US 104-key keyboard.
    # The user should not normally need to use this table,
    # but it is not marked as private.
    #
    # Because the table only goes to 127, we use the top bit of each byte (ox80) to indicate
    # that the shift key should be pressed. So any values 0x{8,9,a,b}* are shifted characters.
    #
    # The Python compiler will concatenate all these bytes literals into a single bytes object.
    # Micropython/CircuitPython will store the resulting bytes constant in flash memory
    # if it's in a .mpy file, so it doesn't use up valuable RAM.
    #
    # \x00 entries have no keyboard key and so won't be sent.
    SHIFT_FLAG = 0x80
    ASCII_TO_KEYCODE = (
        b"\x00"  # NUL 
        b"\x00"  # SOH 
        b"\x00"  # STX 
        b"\x00"  # ETX 
        b"\x00"  # EOT 
        b"\x00"  # ENQ 
        b"\x00"  # ACK 
        b"\x00"  # BEL 
        b"\x2a"  # BS 
        b"\x2b"  # TAB 
        b"\x2b"  # LF 
        b"\x28"  # VT 
        b"\x00"  # FF 
        b"\x00"  # CR 
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
        b"\x20"  # '’ 
        b"\x30"  # $ 
        b"\x00"  # # !ALT+GR
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
        b"\x00"  # @ !alt+gr
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
        b"\x00"  # [ alt+gr
        b"\x00"  # \ alt+gr
        b"\x00"  # ] alt+gr
        b"\x2f"  # ^ 
        b"\x25"  # _ 
        b"\x00"  # ` ???????
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
        b"\x00"  # { altgr
        b"\x00"  # | altgr
        b"\x00"  # } altgr
        b"\x00"  # ~ altgr
        b"\x4c"  # DEL 
    )

    def __init__(self, keyboard):
        """Specify the layout for the given keyboard.

        :param keyboard: a Keyboard object. Write characters to this keyboard when requested.

        Example::

            kbd = Keyboard(usb_hid.devices)
            layout = KeyboardLayoutFR(kbd)
        """

        self.keyboard = keyboard

    def write(self, string):
        """Type the string by pressing and releasing keys on my keyboard.

        :param string: A string of ASCII characters.
        :raises ValueError: if any of the characters are not ASCII or have no keycode
            (such as some control characters).

        Example::

            # Write abc followed by Enter to the keyboard
            layout.write('abc\\n')
        """
        for char in string:
            keycode = self._char_to_keycode(char)
            # If this is a shifted char, clear the SHIFT flag and press the SHIFT key.
            if keycode & self.SHIFT_FLAG:
                keycode &= ~self.SHIFT_FLAG
                self.keyboard.press(Keycode.SHIFT)
            self.keyboard.press(keycode)
            self.keyboard.release_all()

    def keycodes(self, char):
        """Return a tuple of keycodes needed to type the given character.

        :param char: A single ASCII character in a string.
        :type char: str of length one.
        :returns: tuple of Keycode keycodes.
        :raises ValueError: if ``char`` is not ASCII or there is no keycode for it.

        Examples::

            # Returns (Keycode.TAB,)
            keycodes('\t')
            # Returns (Keycode.A,)
            keycode('a')
            # Returns (Keycode.SHIFT, Keycode.A)
            keycode('A')
            # Raises ValueError because it's a accented e and is not ASCII
            keycode('é')
        """
        keycode = self._char_to_keycode(char)
        if keycode & self.SHIFT_FLAG:
            return (Keycode.SHIFT, keycode & ~self.SHIFT_FLAG)

        return (keycode,)

    def _char_to_keycode(self, char):
        """Return the HID keycode for the given ASCII character, with the SHIFT_FLAG possibly set.

        If the character requires pressing the Shift key, the SHIFT_FLAG bit is set.
        You must clear this bit before passing the keycode in a USB report.
        """
        char_val = ord(char)
        if char_val > 128:
            raise ValueError("Not an ASCII character.")
        keycode = self.ASCII_TO_KEYCODE[char_val]
        if keycode == 0:
            raise ValueError("No keycode available for character.")
        return keycode

