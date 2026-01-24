# 🎹 Clavier Macro 6 Touches - RP2040

Un clavier macro programmable avec 6 touches personnalisables, supportant les appuis courts, longs et double-clics. Parfait pour automatiser vos tâches répétitives !

**Petit clavier programmable basé sur RP2040** - 6 exemplaires construits à ce jour.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Matériel requis](#-matériel-requis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Personnalisation](#-personnalisation)
- [Architecture du code](#-architecture-du-code)
- [Dépannage](#-dépannage)

---

## ✨ Fonctionnalités

- **6 touches programmables** avec 3 types d'actions chacune :
  - 🖱️ **Appui court** (< 0.3s)
  - 🖱️🖱️ **Double-clic** (2 appuis rapides)
  - ⏱️ **Appui long** (> 0.3s)
  
- **18 actions personnalisables** au total (6 touches × 3 types)
- **Anti-rebond** matériel pour éviter les faux clics
- **Support clavier AZERTY français** complet avec accents
- **Détection d'erreurs** robuste

### Actions par défaut

| Touche | Court | Long | Double |
|--------|-------|------|--------|
| **0** | Copier (Ctrl+C) | Copier terminal (Ctrl+Shift+C) | - |
| **1** | Coller (Ctrl+V) | Coller terminal (Ctrl+Shift+V) | - |
| **2** | Couper (Ctrl+X) | Supprimer ligne (Ctrl+Shift+K) | - |
| **3** | Annuler (Ctrl+Z) | Refaire (Ctrl+Y) | - |
| **4** | Taper username | Ouvrir terminal + SSH | - |
| **5** | Rechercher (Ctrl+F) | Rechercher/Remplacer (Ctrl+H) | - |

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
├── code.py                    ← Code principal
├── fonctions_touches.py       ← Définition des actions
└── lib/
    └── adafruit_hid/
        └── keyboard_layout_fr.py  ← Layout FR amélioré
```

### 4. Redémarrer

Le RP2040 redémarre automatiquement. Vérifiez dans le serial monitor : `Clavier macro démarré - Prêt à l'emploi`

---

## ⚙️ Configuration

### Modifier les seuils de détection

Dans `code.py` :

```python
DEBOUNCE_TIME = 0.1          # Anti-rebond (100ms)
LONG_PRESS_THRESHOLD = 0.3   # Seuil appui long (300ms)
DOUBLE_CLICK_WINDOW = 0.3    # Fenêtre double-clic (300ms)
```

### Personnaliser vos credentials

Dans `fonctions_touches.py` :

```python
# ============ CONFIGURATION UTILISATEUR ============
USERNAME = 'votre_username'
SSH_USER = 'votre.nom'
SSH_HOST = 'serveur.example.com'
```

---

## 🎮 Utilisation

### Tester les touches

1. Branchez le RP2040 via USB-C
2. Appuyez sur une touche (Cherry MX)
3. Observez la sortie série :
   ```
   Bouton 0 - court
   Bouton 1 - long
   Bouton 2 - double
   ```

### Exemples d'utilisation

**Copier/Coller rapide** :
- Touche 0 court → Copier
- Touche 1 court → Coller

**Connexion SSH automatique** :
- Touche 4 long → Ouvre terminal + `ssh user@host`

**Recherche dans fichier** :
- Touche 5 court → Ctrl+F
- Touche 5 long → Ctrl+H (rechercher/remplacer)

---

## 🎨 Personnalisation

### Ajouter une nouvelle action

Dans `fonctions_touches.py` :

```python
def short2():
    """Nouvelle action pour touche 2 - court"""
    keyboard_layout.write('#!/usr/bin/env python3\n')
    keyboard_layout.write('# -*- coding: utf-8 -*-\n')
```

### Actions disponibles

#### Raccourcis clavier
```python
keyboard.send(Keycode.CONTROL, Keycode.C)  # Ctrl+C
keyboard.send(Keycode.ALT, Keycode.F4)      # Alt+F4
```

#### Taper du texte
```python
keyboard_layout.write('Bonjour !')           # Texte simple
keyboard_layout.write('Email: test@mail.fr') # Avec @
keyboard_layout.write('Prix: 50€')           # Caractères spéciaux
```

#### Texte avec accents français
```python
keyboard_layout.write('Voilà une chaîne accentuée !')
keyboard_layout.write('À très bientôt')
```

#### Séquences complexes
```python
def long4():
    """Ouvre VSCode dans un projet"""
    keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.T)  # Terminal
    sleep(0.5)
    keyboard_layout.write('cd ~/mon-projet\n')
    sleep(0.2)
    keyboard_layout.write('code .\n')
```

### Keycodes disponibles

Les plus utilisés :

```python
# Modificateurs
Keycode.CONTROL / SHIFT / ALT / GUI (Windows/Cmd)
Keycode.RIGHT_ALT  # AltGr

# Navigation
Keycode.ENTER / TAB / ESCAPE / BACKSPACE / DELETE
Keycode.UP_ARROW / DOWN_ARROW / LEFT_ARROW / RIGHT_ARROW
Keycode.HOME / END / PAGE_UP / PAGE_DOWN

# Fonction
Keycode.F1 ... Keycode.F12

# Lettres et chiffres
Keycode.A ... Keycode.Z
Keycode.ONE ... Keycode.ZERO
```

[Liste complète des keycodes](https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode)

---

## 🏗️ Architecture du code

### Structure des fichiers

```
projet/
├── code.py                      # Point d'entrée principal
│   ├── Initialisation boutons
│   ├── Détection des appuis
│   └── Appel des actions
│
├── fonctions_touches.py         # Définition des actions
│   ├── Configuration utilisateur
│   ├── Fonctions short0-5()
│   ├── Fonctions long0-5()
│   └── Fonctions double0-5()
│
└── lib/adafruit_hid/
    └── keyboard_layout_fr.py    # Layout AZERTY amélioré
        ├── Support accents (é, è, à, ù, ç, ê, etc.)
        ├── Support AltGr (#, @, €, [, ], {, })
        └── Dead keys (^ pour accents circonflexes)
```

### Flux d'exécution

```
1. Attente appui touche
2. Identification bouton (0-5)
3. Mesure durée appui
4. Détection double-clic
5. Exécution action correspondante
6. Retour à l'étape 1
```

### Améliorations par rapport à la version originale

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
