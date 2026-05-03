#!/usr/bin/env python3
import sys
import os

# Test minimal pour identifier le problème
print("="*50)
print("TEST DEBUG - Création Window")
print("="*50)

from script_launcher.gui.window import Window

print("\n[1] Avant création Window...")

# Patcher temporairement pour voir où ça bloque
import script_launcher.gui.window as win_module

# Sauvegarder l'init original
original_init = Window.__init__

def debug_init(self, scripts_base_path=None):
    print("[2] Début __init__")
    
    print("[3] Chargement thème...")
    saved_theme = self._load_theme_preference_before_init()
    print(f"    Thème chargé: {saved_theme}")
    
    print("[4] Appel super().__init__()...")
    import ttkbootstrap as ttb
    ttb.Window.__init__(self, themename=saved_theme)
    print("    super().__init__() OK")
    
    print("[5] Configuration titre et géométrie...")
    self.title("🚀 Script Launcher")
    self.geometry("1200x800")
    print("    OK")
    
    print("[6] Configuration variables thèmes...")
    self.themes = ["darkly", "superhero", "cyborg", "solar", "flatly", "litera", "minty", "pulse"]
    try:
        self.current_theme_index = self.themes.index(saved_theme)
    except ValueError:
        self.current_theme_index = 0
    print("    OK")
    
    print("[7] Initialisation gestionnaires...")
    from script_launcher.core.script_manager import ScriptManager
    from script_launcher.core.executor import ScriptExecutor
    
    if scripts_base_path:
        self.script_manager = ScriptManager(base_path=scripts_base_path)
        self.executor = ScriptExecutor(base_path=scripts_base_path)
    else:
        self.script_manager = ScriptManager()
        self.executor = ScriptExecutor()
    print("    OK")
    
    print("[8] Variables script courant...")
    self.current_script = None
    self.current_script_original_name = None
    print("    OK")
    
    print("[9] Appel _setup_ui()...")
    self._setup_ui()
    print("    _setup_ui() OK")
    
    print("[10] Appel _setup_shortcuts()...")
    self._setup_shortcuts()
    print("    _setup_shortcuts() OK")
    
    print("[11] Appel _refresh_script_list()...")
    self._refresh_script_list()
    print("    _refresh_script_list() OK")
    
    print("[12] __init__ terminé avec succès!")

# Remplacer temporairement
Window.__init__ = debug_init

try:
    print("\nCréation de l'objet Window...")
    app = Window(scripts_base_path='./Scripts')
    print("\n✓ SUCCÈS - Fenêtre créée!")
    print("\nFermeture dans 2 secondes...")
    app.after(2000, app.quit)
    app.mainloop()
except Exception as e:
    print(f"\n✗ ERREUR: {e}")
    import traceback
    traceback.print_exc()
