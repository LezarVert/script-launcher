#!/usr/bin/env python3
"""
Script pour lancer l'application Script Launcher
"""
import sys
import os

def check_tkinter():
    """Vérifie que tkinter est installé."""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def get_data_path():
    """Retourne le chemin des données (scripts, config).
    En mode dev : dossier 'scripts' relatif au projet.
    En mode compilé : ~/.local/share/script_launcher/
    """
    if hasattr(sys, '_MEIPASS'):
        # Mode compilé (PyInstaller)
        return os.path.join(os.path.expanduser("~"), ".local", "share", "script_launcher")
    else:
        # Mode développement
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "scripts")

if __name__ == "__main__":
    if not check_tkinter():
        print("❌ Erreur : le module 'tkinter' n'est pas installé.", file=sys.stderr)
        print("\nPour installer les dépendances système :", file=sys.stderr)
        print("  Ubuntu/Debian : sudo apt-get install python3-tk", file=sys.stderr)
        print("  Fedora/RHEL   : sudo dnf install python3-tkinter", file=sys.stderr)
        print("  Arch Linux    : sudo pacman -S tk", file=sys.stderr)
        print("  macOS         : brew install python-tk", file=sys.stderr)
        sys.exit(1)
    
    # Déterminer le chemin des données
    data_path = get_data_path()
    os.makedirs(data_path, exist_ok=True)
    
    # Lancer l'application
    from script_launcher.main import main
    main(scripts_base_path=data_path)