# 🎹 Clavier Macro 6 Touches - RP2040

Un clavier macro programmable avec 6 touches personnalisables, supportant les appuis courts, longs et double-clics. Parfait pour automatiser vos tâches répétitives !

**Petit clavier programmable basé sur RP2040** - 6 exemplaires construits à ce jour.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Matériel requis](#-matériel-requis)
- [Installation](#-installation)
- [Configuration TOML](#-configuration-toml)
- [Utilisation](#-utilisation)
- [Personnalisation](#-personnalisation)
- [Profils disponibles](#-profils-disponibles)
- [Architecture du code](#-architecture-du-code)
- [Dépannage](#-dépannage)

---

## 📂 Profils disponibles

Le fichier `config.toml` inclut 6 profils prêts à l'emploi :

### 1. **default** - Usage général
Copier/Coller, Annuler/Refaire, SSH, Recherche

### 2. **vscode** - Développement
Sidebar, Explorer, Quick open, Command palette, Terminal, Recherche globale

### 3. **terminal** - Ligne de commande
Clear, Sudo, cd/ls, Kill/Exit, SSH, Git status/pull

### 4. **git** - Gestion de version
Status, Log, Add, Commit, Pull, Push, Diff

### 5. **browser** - Navigation web
Nouvel onglet, Fermer, Navigation, Refresh, Favoris, Recherche

### 6. **python** - Développement Python
Headers, Print/Debug, Fonctions/Classes, Try/except, Run/Test, Pip

**Changer de profil** :
```toml
current_profile = "vscode"  # Dans config.toml
```

---

## ✨ Fonctionnalités

- **6 touches programmables** avec 3 types d'actions chacune :
  - 🖱️ **Appui court** (< 0.3s)
  - 🖱️🖱️ **Double-clic** (2 appuis rapides)
  - ⏱️ **Appui long** (> 0.3s)
  
- **18 actions personnalisables** par profil (6 touches × 3 types)
- **Configuration TOML** - Édition facile sans recompiler
- **Profils multiples** - Basculer entre différents ensembles d'actions
- **3 types d'actions** :
  - Raccourcis clavier (Ctrl+C, Alt+F4, etc.)
  - Saisie de texte (email, snippets de code)
  - Commandes spéciales (SSH, scripts)
- **Anti-rebond** matériel pour éviter les faux clics
- **Support clavier AZERTY français** complet avec accents
- **Détection d'erreurs** robuste

### Actions par défaut (Profil "default")

| Touche | Court | Long | Double |
|--------|-------|------|--------|
| **0** | Copier (Ctrl+C) | Copier terminal (Ctrl+Shift+C) | - |
| **1** | Coller (Ctrl+V) | Coller terminal (Ctrl+Shift+V) | - |
| **2** | Couper (Ctrl+X) | Supprimer ligne (Ctrl+Shift+K) | - |
| **3** | Annuler (Ctrl+Z) | Refaire (Ctrl+Y) | - |
| **4** | Taper username | Ouvrir terminal + SSH | - |
| **5** | Rechercher (Ctrl+F) | Rechercher/Remplacer (Ctrl+H) | - |

> **Note** : Toutes les actions sont configurables via `config.toml` sans modifier le code !

---

## 🛠️ Matériel requis

### Composants

- **1× RP2040** 
  - Prototype: RP2040 Zero
  - Production: RP2040 format PicoPi avec USB-C
- **6× Switches Cherry MX** (type au choix: Red, Blue, Brown, etc.)
- **6× PCB breakout Cherry MX** (SparkFun)
  - Produit: [SparkFun Cherry MX Switch Breakout](https://www.sparkfun.com/products/13773)
  - Design open source: [GitHub - SparkFun](https://github.com/sparkfun/Cherry_MX_Switch_Breakout)
- **Câbles** de connexion
- **Boîtier** (optionnel, impression 3D recommandée)

### À propos du hardware

Ce projet utilise des PCB breakout SparkFun (open source) fabriqués en petite série. **6 exemplaires ont été construits** à ce jour, incluant le prototype initial.

Les switches Cherry MX offrent une excellente sensation tactile et une durabilité de plusieurs millions d'actuations.

### Schéma de connexion

```
RP2040 (format PicoPi / Zero)
┌─────────────┐
│   GP0 ●─────┼── Switch 0 (Cherry MX sur breakout) ──┐
│   GP1 ●─────┼── Switch 1 (Cherry MX sur breakout) ──┤
│   GP2 ●─────┼── Switch 2 (Cherry MX sur breakout) ──┤ (vers GND)
│   GP3 ●─────┼── Switch 3 (Cherry MX sur breakout) ──┤
│   GP4 ●─────┼── Switch 4 (Cherry MX sur breakout) ──┤
│   GP5 ●─────┼── Switch 5 (Cherry MX sur breakout) ──┘
│             │
│   GND ●─────┼── Commun (tous les breakouts)
│ USB-C ●     │  Connexion ordinateur
└─────────────┘
```

**Note**: Les PCB SparkFun simplifient grandement le câblage des switches Cherry MX.

### Disposition des touches

```
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
```

---

## 📥 Installation

### 1. Installer CircuitPython

1. Téléchargez [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/) pour RP2040
   - Compatible RP2040 Zero et RP2040 format PicoPi
2. Maintenez le bouton BOOTSEL et branchez le RP2040
3. Copiez le fichier `.uf2` sur le lecteur `RPI-RP2`

### 2. Installer les bibliothèques

Téléchargez le [bundle Adafruit CircuitPython](https://circuitpython.org/libraries) et copiez dans `/lib` :

```
CIRCUITPY/
├── lib/
│   └── adafruit_hid/
│       ├── __init__.py
│       ├── keyboard.py
│       ├── keyboard_layout_fr.py  ← Version améliorée fournie
│       └── keycode.py
```

### 3. Copier les fichiers du projet

```
CIRCUITPY/
├── code.py                    ← Code principal (v3.0 avec TOML)
├── config_manager.py          ← Gestionnaire de configuration
├── config.toml                ← VOTRE CONFIGURATION (éditable)
└── lib/
    └── adafruit_hid/
        ├── keyboard.py
        ├── keyboard_layout_fr.py  ← Layout FR amélioré
        └── keycode.py
```

### 4. Créer la configuration

Au premier lancement, le fichier `config.toml` sera créé automatiquement avec des exemples.

Ou créez-le manuellement en copiant l'exemple fourni.

### 5. Redémarrer

Le RP2040 redémarre automatiquement. Vérifiez dans le serial monitor : 
```
==================================================
Clavier Macro - Version 3.0 avec Config TOML
==================================================
Profil actif: default
Profils disponibles: default, vscode, terminal, git, browser, python
Debounce: 0.1s | Long press: 0.3s
Prêt à l'emploi
==================================================
```

---

## 🎛️ Configuration TOML

### Pourquoi TOML ?

TOML est un format de configuration **ultra-lisible** et **natif à CircuitPython** :

```toml
# Commentaires supportés
[settings]
debounce = 0.1              # Pas de guillemets pour les nombres
long_press = 0.3

[user]
username = "your_name_herer"    # Guillemets pour le texte
ssh_host = "192.168.1.100"
```

**Avantages** :
- ✅ Plus lisible que JSON
- ✅ Support des commentaires
- ✅ Natif CircuitPython (pas de lib externe)
- ✅ Édition en temps réel (redémarrage requis)

### Structure du fichier config.toml

```toml
# ===== PARAMÈTRES GLOBAUX =====
[settings]
debounce = 0.1                # Anti-rebond (secondes)
long_press = 0.3              # Seuil appui long
double_click_window = 0.3     # Fenêtre double-clic

[user]
username = "votre_username"
ssh_user = "votre.nom"
ssh_host = "serveur.example.com"
terminal_delay = 0.5          # Délai ouverture terminal

# Profil actif au démarrage
current_profile = "default"

# ===== PROFILS =====
[profiles.default.button_0]
short = "CTRL+C"              # Raccourci clavier
long = "CTRL+SHIFT+C"
description = "Copier / Copier terminal"

[profiles.default.button_1]
short = { type = "text", action = "mon texte" }  # Taper du texte
long = { type = "command", action = "ssh" }      # Commande spéciale
description = "Texte / SSH"
```

### Types d'actions disponibles

#### 1. Raccourcis clavier (keycombo)

Format simple - juste une string :
```toml
short = "CTRL+C"
long = "CTRL+SHIFT+V"
```

**Modificateurs disponibles** :
- `CTRL` / `CONTROL`
- `SHIFT`
- `ALT`
- `ALTGR` / `RIGHT_ALT`
- `GUI` / `WIN` / `CMD` (touche Windows/Cmd)

**Exemples** :
```toml
"CTRL+C"              # Copier
"CTRL+SHIFT+V"        # Coller sans formatage
"ALT+F4"              # Fermer fenêtre
"GUI+D"               # Afficher bureau (Windows)
"CTRL+ALT+T"          # Ouvrir terminal (Linux)
```

**Touches spéciales** :
- `ENTER`, `TAB`, `ESC`, `BACKSPACE`, `DELETE`
- `UP`, `DOWN`, `LEFT`, `RIGHT`
- `HOME`, `END`, `PAGEUP`, `PAGEDOWN`
- `F1` à `F12`
- Lettres `A` à `Z`
- Chiffres `0` à `9`

#### 2. Saisie de texte (text)

```toml
short = { type = "text", action = "mon.email@example.com" }
long = { type = "text", action = "#!/bin/bash\\nset -euo pipefail\\n" }
```

**Note** : Utilisez `\\n` pour les retours à la ligne (sera converti en Enter)

**Exemples** :
```toml
# Email
{ type = "text", action = "prenom.nom@example.com" }

# Header Python
{ type = "text", action = "#!/usr/bin/env python3\\n# -*- coding: utf-8 -*-\\n\\n" }

# Commande shell
{ type = "text", action = "git status\\n" }

# Username
{ type = "text", action = "your_name_herer" }
```

#### 3. Commandes spéciales (command)

```toml
long = { type = "command", action = "ssh" }
```

**Commandes disponibles** :
- `ssh` : Ouvre un terminal et lance SSH avec vos credentials

**Personnalisation SSH** :
```toml
[user]
ssh_user = "id_ssh"
ssh_host = "192.168.1.100"  # Renseigner votre serveur
```

### Exemples de profils

#### Profil VSCode

```toml
[profiles.vscode.button_0]
short = "CTRL+B"              # Toggle sidebar
long = "CTRL+SHIFT+E"         # Explorer
description = "Sidebar / Explorer"

[profiles.vscode.button_1]
short = "CTRL+P"              # Quick open
long = "CTRL+SHIFT+P"         # Command palette
description = "Quick open / Palette"
```

#### Profil Git

```toml
[profiles.git.button_0]
short = { type = "text", action = "git status\\n" }
long = { type = "text", action = "git log --oneline -10\\n" }
description = "Status / Log"

[profiles.git.button_1]
short = { type = "text", action = "git add .\\n" }
long = { type = "text", action = "git commit -m \\"" }  # Positionne pour écrire le message
description = "Add / Commit"
```

#### Profil Python

```toml
[profiles.python.button_0]
short = { type = "text", action = "#!/usr/bin/env python3\\n# -*- coding: utf-8 -*-\\n\\n" }
long = { type = "text", action = "if __name__ == '__main__':\\n    " }
description = "Header / Main"

[profiles.python.button_1]
short = { type = "text", action = "print()" }
long = { type = "text", action = "import pdb; pdb.set_trace()" }
description = "Print / Debugger"
```

### Changer de profil

**Méthode 1 : Éditer config.toml**

```toml
current_profile = "vscode"  # Changer ici
```

Sauvegarder et redémarrer le RP2040.

**Méthode 2 : Programmation (à venir)**

Ajouter une touche pour cycler entre profils :
```toml
[profiles.default.button_5]
double = { type = "command", action = "cycle_profile" }
```

### Créer votre propre profil

```toml
[profiles.mon_profil.button_0]
short = "CTRL+C"
long = { type = "text", action = "Mon texte personnalisé" }
description = "Ma description"

[profiles.mon_profil.button_1]
short = "CTRL+V"
# ... etc pour les 6 boutons
```

Puis activez-le :
```toml
current_profile = "mon_profil"
```

---

## ⚙️ Configuration (ancienne méthode)

> **Note** : Depuis la version 3.0, utilisez plutôt `config.toml` (voir section précédente)

### Modifier les seuils de détection

Dans `code.py` :

```python
DEBOUNCE_TIME = 0.1          # Anti-rebond (100ms)
LONG_PRESS_THRESHOLD = 0.3   # Seuil appui long (300ms)
DOUBLE_CLICK_WINDOW = 0.3    # Fenêtre double-clic (300ms)
```

### Personnaliser vos credentials

Dans `config.toml` :

```toml
[user]
username = "votre_username"
ssh_user = "votre.nom"
ssh_host = "serveur.example.com"
```

---

## 🎮 Utilisation

### Tester les touches

1. Branchez le RP2040 via USB-C
2. Appuyez sur une touche (Cherry MX)
3. Observez la sortie série :
   ```
   [default] Bouton 0 - court: Copier / Copier terminal
   [default] Bouton 1 - long: Coller / Coller terminal
   [default] Bouton 2 - double: N/A
   ```

### Exemples d'utilisation

**Copier/Coller rapide** (profil default) :
- Touche 0 court → Copier (Ctrl+C)
- Touche 1 court → Coller (Ctrl+V)

**Connexion SSH automatique** (profil default) :
- Touche 4 long → Ouvre terminal + `ssh user@host`

**Workflow Git** (profil git) :
- Touche 0 court → `git status`
- Touche 1 court → `git add .`
- Touche 2 court → `git commit -m ""`

**Développement VSCode** (profil vscode) :
- Touche 0 court → Toggle sidebar (Ctrl+B)
- Touche 1 long → Command palette (Ctrl+Shift+P)

### Changer de profil

Éditez `config.toml` et changez :
```toml
current_profile = "vscode"  # ou "terminal", "git", "browser", "python"
```

Sauvegardez et redémarrez le RP2040 (débrancher/rebrancher ou touche reset).

---

## 🎨 Personnalisation

> **Version 3.0** : Toute la personnalisation se fait via `config.toml` !

### Ajouter une nouvelle action

Éditez `config.toml` :

```toml
[profiles.default.button_2]
short = { type = "text", action = "#!/usr/bin/env python3\\n# -*- coding: utf-8 -*-\\n" }
long = "CTRL+SHIFT+K"
description = "Python header / Supprimer ligne"
```

Sauvegardez, redémarrez le RP2040. C'est tout ! 🎉

### Actions disponibles

Voir la section [Configuration TOML](#️-configuration-toml) pour la liste complète.

**Raccourcis rapides** :

```toml
# Raccourci clavier simple
short = "CTRL+C"

# Taper du texte
short = { type = "text", action = "mon texte" }

# Commande spéciale
long = { type = "command", action = "ssh" }
```

### Créer un profil personnalisé

```toml
[profiles.mon_workflow.button_0]
short = { type = "text", action = "npm start\\n" }
long = { type = "text", action = "npm test\\n" }
description = "Start / Test"

# ... définir les 6 boutons

# Activer le profil
current_profile = "mon_workflow"
```

---

## 🏗️ Architecture du code

### Structure des fichiers

```
projet/
├── code.py                      # Point d'entrée principal (v3.0)
│   ├── Chargement config TOML
│   ├── Initialisation boutons
│   ├── Détection des appuis
│   └── Exécution des actions
│
├── config_manager.py            # Gestionnaire de configuration
│   ├── Parsing TOML
│   ├── Validation config
│   ├── Conversion keycodes
│   └── Gestion profils
│
├── config.toml                  # CONFIGURATION UTILISATEUR
│   ├── Paramètres globaux
│   ├── Credentials utilisateur
│   └── Définition des profils
│
└── lib/adafruit_hid/
    ├── keyboard.py              # HID keyboard
    ├── keycode.py               # Keycodes
    └── keyboard_layout_fr.py    # Layout AZERTY amélioré
        ├── Support accents (é, è, à, ù, ç, ê, etc.)
        ├── Support AltGr (#, @, €, [, ], {, })
        └── Dead keys (^ pour accents circonflexes)
```

### Flux d'exécution

```
1. Chargement config.toml
2. Initialisation HID + boutons
3. Attente appui touche
4. Identification bouton (0-5)
5. Mesure durée appui
6. Détection double-clic
7. Récupération action depuis config
8. Exécution selon type (keycombo/text/command)
9. Retour à l'étape 3
```

### Améliorations par rapport aux versions précédentes

**Version 3.0 (2026-01-24)** :
✅ Configuration TOML complète  
✅ Profils multiples (6 inclus)  
✅ 3 types d'actions (keycombo, text, command)  
✅ Plus besoin de modifier le code Python  
✅ Gestionnaire de config dédié  

**Version 2.0 (2026-01-24)** :
✅ Code refactorisé (réduction 50% de lignes)  
✅ Utilisation de listes au lieu de variables séparées  
✅ Dictionnaire d'actions au lieu de cascades if/elif  
✅ Gestion d'erreurs robuste  
✅ Support complet accents français  
✅ Support caractères AltGr  
✅ Constantes nommées pour configuration  
✅ Documentation complète  

---

## 🐛 Dépannage

### Le clavier ne répond pas

**Vérifier** :
- Le RP2040 est bien alimenté (LED allumée)
- Les switches Cherry MX sont bien connectés aux GPIO via les breakouts
- CircuitPython est bien installé
- Les fichiers sont dans `CIRCUITPY/` (pas dans un sous-dossier)

**Solution** :
```python
# Dans code.py, ajouter des prints pour debug
print(f'Bouton détecté: {button_pressed}')
```

### Double-clics non détectés

**Cause** : Fenêtre de détection trop courte

**Solution** :
```python
# Dans code.py
DOUBLE_CLICK_WINDOW = 0.5  # Augmenter à 500ms
```

### Caractères accentués incorrects

**Cause** : Layout clavier incorrect sur l'ordinateur

**Solution** : Vérifiez que votre OS est configuré en AZERTY français

### Erreur "No module named 'adafruit_hid'"

**Cause** : Bibliothèques manquantes

**Solution** :
1. Téléchargez le [bundle CircuitPython](https://circuitpython.org/libraries)
2. Copiez le dossier `adafruit_hid/` dans `CIRCUITPY/lib/`

### Erreur config.toml

**Symptôme** : `⚠ Fichier config.toml non trouvé`

**Solution** :
1. Créez le fichier manuellement ou
2. Dans `code.py`, décommentez : `config.create_default_config()`
3. Relancez, un fichier d'exemple sera créé

### Actions ne fonctionnent pas

**Vérifier** :
1. La syntaxe TOML est correcte (pas d'erreur au chargement)
2. Le profil actif contient bien les actions
3. Les keycodes sont valides (voir liste dans config TOML)

**Debug** :
```bash
# Voir les logs série
screen /dev/ttyACM0 115200
# ou
minicom -D /dev/ttyACM0 -b 115200
```

### Les touches rebondissent (faux clics)

**Solution** :
```python
# Augmenter le debounce
DEBOUNCE_TIME = 0.15  # 150ms au lieu de 100ms
```

### Le Pico se monte en lecture seule (filesystem corrompu)

**Cause** : Débranchement brutal alors que des fichiers étaient ouverts sur Linux

**Solution** (Linux) :
```bash
# 1. Identifier le périphérique
lsblk
# Repérer le point de montage (ex: /media/user/CIRCUITPY -> /dev/sdb1)

# 2. Démonter le filesystem
sudo umount /media/user/CIRCUITPY

# 3. Réparer le filesystem FAT
sudo dosfsck -a /dev/sdb1
# Remplacer sdb1 par votre périphérique identifié à l'étape 1

# 4. Débrancher et rebrancher le RP2040
```

**Prévention** : Toujours éjecter proprement le RP2040 avant de le débrancher (surtout sur Linux)

---

## 📚 Ressources

### Documentation
- [Documentation CircuitPython](https://docs.circuitpython.org/)
- [Adafruit HID Library](https://circuitpython.readthedocs.io/projects/hid/en/latest/)
- [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
- [Guide Adafruit - Macro Keyboards](https://learn.adafruit.com/custom-hid-devices-in-circuitpython)

### Hardware
- [SparkFun Cherry MX Breakout](https://www.sparkfun.com/products/13773)
- [Repo GitHub SparkFun (Open Source)](https://github.com/sparkfun/Cherry_MX_Switch_Breakout)
- [Cherry MX Switches - Guide complet](https://www.cherrymx.de/en/cherry-mx.html)

---

## 📝 Changelog

### Version 3.0 (2026-01-24)
- ✨ **Configuration TOML** - Toute la config externalisée
- ✨ **Profils multiples** - 6 profils inclus (default, vscode, terminal, git, browser, python)
- ✨ **3 types d'actions** - keycombo, text, command
- ✨ **Gestionnaire de config** - Module config_manager.py dédié
- ✨ **Plus besoin de coder** - Tout se configure en TOML
- 🔧 Parsing intelligent des raccourcis clavier
- 🔧 Validation et messages d'erreur clairs
- 📚 Documentation TOML complète

### Version 2.0 (2026-01-24)
- ✨ Refonte complète du code
- ✨ Support accents français complet
- ✨ Support caractères AltGr
- ✨ Détection double-clic
- ✨ Gestion d'erreurs robuste
- ✨ Architecture modulaire
- 📚 Documentation complète

### Version 1.0 (2022-08-23)
- 🎉 Version initiale
- ⌨️ 6 touches avec appui court/long
- 🇫🇷 Layout AZERTY de base

---

## 👤 Auteur

**Hugues Goussard**
- 📧 Email: hugues.goussard@gmail.com
- 💼 Projet personnel - Automatisation workflow
- 📅 Création initiale: 23 août 2022
- 🔄 Refonte majeure: 24 janvier 2026

---

## 📄 Licence

MIT License - Libre d'utilisation et modification

---

## 🙏 Remerciements

- **Adafruit** pour les bibliothèques CircuitPython HID
- **Dan Halbert** pour le layout clavier original US
- **Claude (Anthropic)** pour l'assistance au refactoring et l'amélioration du layout FR
- **SparkFun** pour les PCB breakout Cherry MX en open source
- **Communauté CircuitPython** pour la documentation et les exemples
- **Raspberry Pi Foundation** pour le RP2040

### Contributions

Ce projet a bénéficié d'une refonte majeure en janvier 2026 incluant :
- Refactorisation complète du code principal
- Amélioration du layout clavier français avec support accents et AltGr
- Ajout de la détection double-clic
- Documentation exhaustive
- Gestion d'erreurs robuste

### Production

**6 exemplaires construits** (prototype RP2040 Zero + 5 versions USB-C format PicoPi) utilisant des PCB SparkFun fabriqués en petite série.

---

**Bon coding ! 🚀**