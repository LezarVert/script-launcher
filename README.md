# 🚀 Script Launcher

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyInstaller](https://img.shields.io/badge/build-PyInstaller-orange.svg)]()

Une application GUI moderne pour gérer, éditer et exécuter vos scripts Python et Shell.

![Script Launcher Screenshot](assets/screenshot.png)

## ✨ Fonctionnalités

### 🎯 Gestion des Scripts
- **Création** de scripts Python (.py) ou Shell (.sh) avec métadonnées
- **Édition** de code avec interface intuitive
- **Exécution** avec capture de sortie en temps réel
- **Suppression** avec confirmation
- **Renommage** automatique des fichiers

### 🎨 Interface Moderne
- **Thèmes multiples** : darkly, superhero, solar, flatly
- **Barre latérale** avec liste de scripts et icônes
- **Éditeur de code** avec métadonnées
- **Console intégrée** pour les sorties d'exécution
- **Barre de recherche** avec filtrage en temps réel

### ⌨️ Raccourcis Clavier
| Raccourci | Action |
|-----------|--------|
| `Ctrl+S` | Sauvegarder le script |
| `F5` | Exécuter le script |
| `Ctrl+F` | Focus sur la recherche |
| `Ctrl+N` | Nouveau script |
| `Ctrl+Q` | Quitter l'application |

### 📊 Suivi et Métadonnées
- Dates de création, modification, exécution
- Historique des exécutions
- Fichiers de métadonnées JSON par script

## 🏗️ Architecture

Le projet suit le pattern **MVC** (Model-View-Controller) :

```
script_launcher/
├── main.py                 # Point d'entrée
├── gui/                    # Vue (Interface graphique)
│   ├── window.py          # Fenêtre principale (Contrôleur)
│   └── widgets/
│       ├── script_list.py # Liste des scripts
│       ├── script_editor.py # Éditeur de code
│       └── console_log.py # Console de sortie
├── core/                   # Modèle (Logique métier)
│   ├── script_manager.py  # Gestion CRUD des scripts
│   └── executor.py        # Exécution des scripts
└── utils/                  # Utilitaires
    └── logger.py          # Système de logging
```

## 🚀 Installation

### Prérequis
- Python 3.10+
- Tkinter (inclus dans la plupart des installations Python)

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/LezarVert/script-launcher.git
cd script-launcher/dev-tools-python

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Dépendances système (Linux)
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

## 💻 Utilisation

### Mode développement
```bash
cd dev-tools-python
python run.py
```

### Via le script shell (Linux)
```bash
cd dev-tools-python
chmod +x run.sh
./run.sh
```

### Build avec PyInstaller

Le fichier `.spec` est déjà configuré avec les imports cachés nécessaires :

```bash
# Installer PyInstaller
pip install pyinstaller

# Compiler l'application
cd dev-tools-python
pyinstaller ScriptLauncher.spec

# L'exécutable sera dans dist/ScriptLauncher
```

### Import caché important
Si vous compilez manuellement, n'oubliez pas d'inclure l'import caché de Pillow :
```bash
pyinstaller --hidden-import PIL._tkinter_finder --onefile --windowed run.py
```

### Installation
Création du fichier de raccourci :
```bash
[Desktop Entry]
Type=Application
Name=Script Launcher
Comment=Gestionnaire de scripts Python
Exec=/home/[user-name]/Outils/devtools/dev-tools-python/run.py
Icon=accessories-text-editor
Terminal=false
Categories=Development;Utility;
StartupNotify=true
```

## 📁 Structure des Scripts

Chaque script est stocké dans un dossier avec la structure suivante :

```
scripts/
└── mon_script/
    ├── meta.json          # Métadonnées (nom, description, auteur)
    ├── main.py ou main.sh # Code du script
    └── log.txt           # Historique d'exécution
```

### Format de meta.json
```json
{
    "name": "Mon Script",
    "description": "Description du script",
    "author": "Votre Nom",
    "type": "python",
    "created_at": "2026-05-03T10:00:00",
    "last_executed": "2026-05-03T11:00:00",
    "last_modified": "2026-05-03T10:30:00"
}
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails.

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.

## 🙏 Remerciements

- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) pour les thèmes modernes
- [Pillow](https://python-pillow.org/) pour la gestion des images
- [PyInstaller](https://www.pyinstaller.org/) pour la compilation

## 🐛 Signaler un Bug

Si vous rencontrez un problème, veuillez ouvrir une [issue](https://github.com/LezarVert/script-launcher/issues) en incluant :
- Votre système d'exploitation
- La version de Python
- Les étapes pour reproduire le bug
- Des captures d'écran si possible

## 📧 Contact

Vincent Desbeaux - [site web](https://vi-de-web.fr)

Lien du projet : [https://github.com/LezarVert/script-launcher](https://github.com/LezarVert/script-launcher)
