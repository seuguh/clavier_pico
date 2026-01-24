"""
config_manager.py
=================
Gestionnaire de configuration TOML pour le clavier macro

Charge et applique les paramètres depuis config.toml
"""

try:
    import toml
except ImportError:
    print("ERREUR: Module toml non disponible")
    print("Assurez-vous d'avoir CircuitPython 8.0+")
    raise

from adafruit_hid.keycode import Keycode


class ConfigManager:
    """Gère le chargement et la validation de la configuration TOML"""
    
    DEFAULT_CONFIG_PATH = 'config.toml'
    
    # Valeurs par défaut si config.toml manque
    DEFAULTS = {
        'settings': {
            'debounce': 0.1,
            'long_press': 0.3,
            'double_click_window': 0.3,
        },
        'user': {
            'username': '',
            'ssh_user': '',
            'ssh_host': '',
            'terminal_delay': 0.5,
        },
        'current_profile': 'default',
    }
    
    # Mapping texte → Keycode
    KEYCODE_MAP = {
        'CTRL': Keycode.CONTROL,
        'CONTROL': Keycode.CONTROL,
        'SHIFT': Keycode.SHIFT,
        'ALT': Keycode.ALT,
        'ALTGR': Keycode.RIGHT_ALT,
        'RIGHT_ALT': Keycode.RIGHT_ALT,
        'GUI': Keycode.GUI,
        'WIN': Keycode.GUI,
        'CMD': Keycode.GUI,
        'ENTER': Keycode.ENTER,
        'TAB': Keycode.TAB,
        'ESC': Keycode.ESCAPE,
        'ESCAPE': Keycode.ESCAPE,
        'BACKSPACE': Keycode.BACKSPACE,
        'DELETE': Keycode.DELETE,
        'UP': Keycode.UP_ARROW,
        'DOWN': Keycode.DOWN_ARROW,
        'LEFT': Keycode.LEFT_ARROW,
        'RIGHT': Keycode.RIGHT_ARROW,
        'HOME': Keycode.HOME,
        'END': Keycode.END,
        'PAGEUP': Keycode.PAGE_UP,
        'PAGEDOWN': Keycode.PAGE_DOWN,
        'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
        'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6,
        'F7': Keycode.F7, 'F8': Keycode.F8, 'F9': Keycode.F9,
        'F10': Keycode.F10, 'F11': Keycode.F11, 'F12': Keycode.F12,
    }
    
    # Ajouter les lettres A-Z
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        KEYCODE_MAP[letter] = getattr(Keycode, letter)
    
    # Ajouter les chiffres 0-9
    for num in '0123456789':
        digit_names = {
            '0': 'ZERO', '1': 'ONE', '2': 'TWO', '3': 'THREE',
            '4': 'FOUR', '5': 'FIVE', '6': 'SIX', '7': 'SEVEN',
            '8': 'EIGHT', '9': 'NINE'
        }
        KEYCODE_MAP[num] = getattr(Keycode, digit_names[num])
    
    def __init__(self, config_path=None):
        """Initialise et charge la configuration
        
        Args:
            config_path: Chemin vers le fichier TOML (défaut: config.toml)
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self.DEFAULTS.copy()
        self.load()
    
    def load(self):
        """Charge la configuration depuis le fichier TOML"""
        try:
            with open(self.config_path, 'r') as f:
                loaded = toml.load(f)
                # Fusionner avec les valeurs par défaut
                self._merge_config(loaded)
                print(f'✓ Configuration chargée depuis {self.config_path}')
                return True
        except OSError:
            print(f'⚠ Fichier {self.config_path} non trouvé, utilisation des valeurs par défaut')
            return False
        except Exception as e:
            print(f'✗ Erreur lecture config: {e}')
            return False
    
    def _merge_config(self, loaded):
        """Fusionne la config chargée avec les defaults"""
        for key, value in loaded.items():
            if isinstance(value, dict) and key in self.config:
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, *keys, default=None):
        """Récupère une valeur de config avec navigation par clés
        
        Args:
            *keys: Chemin vers la valeur (ex: 'settings', 'debounce')
            default: Valeur par défaut si clé non trouvée
            
        Returns:
            La valeur trouvée ou default
            
        Example:
            config.get('settings', 'debounce')  # → 0.1
        """
        current = self.config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def parse_keycombo(self, combo_string):
        """Parse une combo de touches depuis une string
        
        Args:
            combo_string: String type "CTRL+SHIFT+C" ou "ALT+F4"
            
        Returns:
            Liste de Keycode objects
            
        Example:
            parse_keycombo("CTRL+C")  # → [Keycode.CONTROL, Keycode.C]
        """
        if not combo_string:
            return []
        
        parts = [p.strip().upper() for p in combo_string.split('+')]
        keycodes = []
        
        for part in parts:
            if part in self.KEYCODE_MAP:
                keycodes.append(self.KEYCODE_MAP[part])
            else:
                print(f'⚠ Keycode inconnu: {part}')
        
        return keycodes
    
    def get_profile(self, profile_name=None):
        """Récupère un profil complet
        
        Args:
            profile_name: Nom du profil (défaut: profil actuel)
            
        Returns:
            Dict du profil ou None
        """
        if profile_name is None:
            profile_name = self.config.get('current_profile', 'default')
        
        profiles = self.config.get('profiles', {})
        return profiles.get(profile_name)
    
    def get_button_action(self, button_num, click_type, profile_name=None):
        """Récupère l'action d'un bouton
        
        Args:
            button_num: Numéro du bouton (0-5)
            click_type: 'short', 'long', ou 'double'
            profile_name: Nom du profil (optionnel)
            
        Returns:
            Dict avec 'action', 'description', 'type' ou None
        """
        profile = self.get_profile(profile_name)
        if not profile:
            return None
        
        button_key = f'button_{button_num}'
        if button_key not in profile:
            return None
        
        button_config = profile[button_key]
        if click_type not in button_config:
            return None
        
        action = button_config[click_type]
        
        # Si c'est juste une string, c'est un raccourci clavier
        if isinstance(action, str):
            return {
                'type': 'keycombo',
                'action': action,
                'description': button_config.get('description', '')
            }
        
        # Si c'est un dict, récupérer le type d'action
        if isinstance(action, dict):
            return {
                'type': action.get('type', 'keycombo'),
                'action': action.get('action', ''),
                'description': action.get('description', '')
            }
        
        return None
    
    def list_profiles(self):
        """Liste tous les profils disponibles
        
        Returns:
            Liste des noms de profils
        """
        return list(self.config.get('profiles', {}).keys())
    
    def switch_profile(self, profile_name):
        """Change le profil actif
        
        Args:
            profile_name: Nom du profil à activer
            
        Returns:
            True si succès, False sinon
        """
        if profile_name in self.list_profiles():
            self.config['current_profile'] = profile_name
            print(f'✓ Profil actif: {profile_name}')
            return True
        else:
            print(f'✗ Profil inconnu: {profile_name}')
            return False
    
    def create_default_config(self, path=None):
        """Crée un fichier de config par défaut
        
        Args:
            path: Chemin du fichier (défaut: config.toml)
        """
        path = path or self.config_path
        
        default_toml = '''# Configuration du clavier macro
# Édité manuellement - Redémarrer le RP2040 après modification

[settings]
debounce = 0.1                # Anti-rebond en secondes
long_press = 0.3              # Seuil appui long en secondes
double_click_window = 0.3     # Fenêtre détection double-clic

[user]
username = "your_name_herer"
ssh_user = "id_ssh"
ssh_host = ""                 # Renseigner l'adresse du serveur
terminal_delay = 0.5          # Délai ouverture terminal

# Profil actif au démarrage
current_profile = "default"

# ============================================================
# PROFILS - Définition des actions par touche
# ============================================================
# Format des raccourcis clavier: "MODIFICATEUR+TOUCHE"
# Modificateurs: CTRL, SHIFT, ALT, ALTGR, GUI/WIN/CMD
# Exemples: "CTRL+C", "CTRL+SHIFT+V", "ALT+F4"
#
# Types d'actions:
# - keycombo: Raccourci clavier (par défaut)
# - text: Taper du texte
# - command: Commande shell (avec terminal)
# ============================================================

[profiles.default.button_0]
short = "CTRL+C"
long = "CTRL+SHIFT+C"
description = "Copier / Copier terminal"

[profiles.default.button_1]
short = "CTRL+V"
long = "CTRL+SHIFT+V"
description = "Coller / Coller terminal"

[profiles.default.button_2]
short = "CTRL+X"
long = "CTRL+SHIFT+K"
description = "Couper / Supprimer ligne"

[profiles.default.button_3]
short = "CTRL+Z"
long = "CTRL+Y"
description = "Annuler / Refaire"

[profiles.default.button_4]
short = { type = "text", action = "your_name_herer" }
long = { type = "command", action = "ssh" }
description = "Username / SSH"

[profiles.default.button_5]
short = "CTRL+F"
long = "CTRL+H"
description = "Rechercher / Remplacer"

# Profil VSCode
[profiles.vscode.button_0]
short = "CTRL+B"
long = "CTRL+SHIFT+E"
description = "Toggle sidebar / Explorer"

[profiles.vscode.button_1]
short = "CTRL+P"
long = "CTRL+SHIFT+P"
description = "Quick open / Command palette"

[profiles.vscode.button_2]
short = "CTRL+D"
long = "CTRL+SHIFT+L"
description = "Selection / Tout sélectionner"

[profiles.vscode.button_3]
short = "CTRL+Z"
long = "CTRL+SHIFT+Z"
description = "Undo / Redo"

[profiles.vscode.button_4]
short = "CTRL+SHIFT+GRAVE_ACCENT"  # Grave accent = `
long = "F5"
description = "Terminal / Debug"

[profiles.vscode.button_5]
short = "CTRL+F"
long = "CTRL+SHIFT+F"
description = "Recherche / Recherche globale"

# Profil Terminal
[profiles.terminal.button_0]
short = { type = "text", action = "clear\\n" }
long = { type = "text", action = "sudo " }
description = "Clear / Sudo"

[profiles.terminal.button_1]
short = "CTRL+SHIFT+V"
long = "CTRL+SHIFT+C"
description = "Coller / Copier"

[profiles.terminal.button_2]
short = { type = "text", action = "cd .." }
long = { type = "text", action = "ls -lah\\n" }
description = "cd .. / ls"

[profiles.terminal.button_3]
short = "CTRL+C"
long = "CTRL+D"
description = "Kill / Exit"

[profiles.terminal.button_4]
short = { type = "command", action = "ssh" }
long = { type = "text", action = "history\\n" }
description = "SSH / History"

[profiles.terminal.button_5]
short = { type = "text", action = "git status\\n" }
long = { type = "text", action = "git pull\\n" }
description = "Git status / Git pull"
'''
        
        try:
            with open(path, 'w') as f:
                f.write(default_toml)
            print(f'✓ Fichier de config créé: {path}')
            return True
        except Exception as e:
            print(f'✗ Erreur création config: {e}')
            return False


# Fonction utilitaire pour l'utiliser facilement
def load_config(path=None):
    """Charge la configuration (fonction helper)
    
    Args:
        path: Chemin optionnel vers le fichier TOML
        
    Returns:
        Instance de ConfigManager
    """
    return ConfigManager(path)


# ========== EXEMPLE D'UTILISATION ==========
if __name__ == '__main__':
    # Charger la config
    config = ConfigManager()
    
    # Ou créer un fichier par défaut
    # config.create_default_config()
    
    # Accéder aux paramètres
    print(f"Debounce: {config.get('settings', 'debounce')}")
    print(f"Username: {config.get('user', 'username')}")
    
    # Parser un raccourci clavier
    combo = config.parse_keycombo("CTRL+SHIFT+C")
    print(f"Keycodes: {combo}")
    
    # Récupérer une action de bouton
    action = config.get_button_action(0, 'short')
    print(f"Bouton 0 court: {action}")
    
    # Lister les profils
    print(f"Profils: {config.list_profiles()}")
    
    # Changer de profil
    config.switch_profile('vscode')