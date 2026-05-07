"""
Script Launcher - Gestionnaire de scripts Python
"""

import tkinter as tk
import os
import sys

# Ajouter le répertoire parent au path pour permettre les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from script_launcher.gui.window import Window

def main(scripts_base_path=None):
    """Point d'entrée de l'application."""
    # Déterminer le répertoire de base de l'application
    if scripts_base_path is None:
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        scripts_base_path = os.path.join(app_dir, "scripts")

    os.makedirs(scripts_base_path, exist_ok=True)
    
    app = Window(scripts_base_path=scripts_base_path)
    app.mainloop()

if __name__ == "__main__":
    main()