import tkinter as tk
from tkinter import messagebox
from typing import Dict, Optional
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import json
import os
import threading
import sys

from script_launcher.core.script_manager import ScriptManager
from script_launcher.core.executor import ScriptExecutor
from script_launcher.gui.widgets import ScriptList, ScriptEditor

class Window(ttk.Window):
    def __init__(self, scripts_base_path: Optional[str] = None):
        """Initialise la fenêtre principale.
        
        Args:
            scripts_base_path (Optional[str]): Chemin de base pour les scripts
        """
        # Charger le thème sauvegardé AVANT l'initialisation
        saved_theme = self._load_theme_preference_static()
        
        # Initialiser avec le thème sauvegardé ou darkly par défaut
        super().__init__(themename=saved_theme if saved_theme else "darkly")

        def get_resource_path(relative_path):
            """Obtient le chemin absolu, que ce soit en mode dev ou compilé."""
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), relative_path)
    
         # Définir l'icône de l'application (fusée)
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Essayer PNG d'abord (Linux/Mac)
            # icon_path = os.path.join(base_path, "assets", "rocket.png")
            icon_path = get_resource_path("assets/rocket.png")
            if os.path.exists(icon_path):
                icon_img = tk.PhotoImage(file=icon_path)
                self.iconphoto(True, icon_img)
            else:
                # Fallback sur ICO (Windows)
                icon_path = get_resource_path("assets/rocket.ico")
                if os.path.exists(icon_path):
                    self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Impossible de charger l'icône: {e}")
        
        # Configuration de la fenêtre principale
        self.title("Script Launcher")
        self.geometry("1400x1024")
        self.minsize(1400, 1024)
        
        self.title("🚀 Script Launcher")
        self.geometry("1200x800")
        
        # Liste des thèmes disponibles
        self.themes = ["darkly", "superhero", "solar", "flatly"]
        
        # Définir l'index du thème actuel
        if saved_theme and saved_theme in self.themes:
            self.current_theme_index = self.themes.index(saved_theme)
        else:
            self.current_theme_index = 0
        
        # Initialiser les gestionnaires avec le chemin spécifié
        if scripts_base_path:
            self.script_manager = ScriptManager(base_path=scripts_base_path)
            self.executor = ScriptExecutor(base_path=scripts_base_path)
        else:
            self.script_manager = ScriptManager()
            self.executor = ScriptExecutor()
        
        # Variable pour le script courant
        self.current_script: Optional[str] = None
        self.current_script_original_name: Optional[str] = None  # Nom original pour détecter les changements
        
        self._setup_ui()
        self._setup_shortcuts()
        
        # Forcer l'affichage de la fenêtre et restaurer le curseur normal
        self.update_idletasks()
        self.update()
        self.config(cursor="")  # Restaurer le curseur par défaut
        
        # Charger les scripts après l'affichage de la fenêtre
        self.after(100, self._load_scripts_async)

    
    def _load_theme_preference_static(self) -> str:
        """Charge le thème sauvegardé AVANT l'init de manière statique."""
        try:
            # Calculer le chemin sans self
            import os
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_dir = os.path.join(app_dir, ".config")
            config_file = os.path.join(config_dir, "preferences.json")
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("theme", "darkly")
        except Exception:
            pass
        return "darkly"
    
    def _load_theme_preference_before_init(self) -> str:
        """Charge le thème sauvegardé AVANT l'init (version simple sans self)."""
        try:
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_dir = os.path.join(app_dir, ".config")
            config_file = os.path.join(config_dir, "preferences.json")
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("theme", "darkly")
        except Exception:
            pass
        return "darkly"
    
    def _get_config_file(self) -> str:
        """Retourne le chemin du fichier de configuration."""
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_dir = os.path.join(app_dir, ".config")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "preferences.json")
    
    def _load_theme_preference(self) -> str:
        """Charge le thème sauvegardé ou retourne le thème par défaut."""
        try:
            config_file = self._get_config_file()
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("theme", "darkly")
        except Exception:
            pass
        return "darkly"
    
    def _save_theme_preference(self, theme: str):
        """Sauvegarde le thème dans le fichier de configuration."""
        try:
            config_file = self._get_config_file()
            config = {}
            # Charger la config existante si elle existe
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
            # Mettre à jour le thème
            config["theme"] = theme
            # Sauvegarder
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des préférences: {e}")
    
    def _toggle_theme(self):
        """Cycle entre les différents thèmes disponibles."""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        new_theme = self.themes[self.current_theme_index]
        self.style.theme_use(new_theme)
        self.theme_button.configure(text=f"🎨 {new_theme.title()}")
        # Sauvegarder le thème
        self._save_theme_preference(new_theme)
        
    def _setup_shortcuts(self):
        """Configure les raccourcis clavier."""
        # Sauvegarde (Ctrl+S)
        self.bind_all("<Control-s>", lambda e: self._save_current_script())
        
        # Exécution (F5)
        self.bind_all("<F5>", lambda e: self._run_current_script())
        
        # Recherche (Ctrl+F)
        self.bind_all("<Control-f>", self._focus_search)
        
        # Nouveau script (Ctrl+N)
        self.bind_all("<Control-n>", lambda e: self._new_script_dialog())
        
        # Quitter l'application (Ctrl+Q)
        self.bind_all("<Control-q>", lambda e: self.quit())
        
    def _focus_search(self, event=None):
        """Place le focus sur la barre de recherche."""
        if hasattr(self, 'script_list') and hasattr(self.script_list, 'search_entry'):
            self.script_list.search_entry.focus_set()
            # Sélectionner tout le texte sauf si c'est le placeholder
            if self.script_list.search_var.get() != "Rechercher...":
                self.script_list.search_entry.selection_range(0, tk.END)
        
    def _setup_ui(self):
        """Configure une interface utilisateur moderne et épurée."""
        # Conteneur principal avec grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # === ZONE PRINCIPALE DROITE (créée en premier pour les callbacks) ===
        right_frame = ttk.Frame(self, padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_frame.grid_rowconfigure(1, weight=3)  # Éditeur (row 1)  
        right_frame.grid_rowconfigure(2, weight=0)  # Boutons (row 2) - pas de poids
        right_frame.grid_rowconfigure(3, weight=0)  # Console header (row 3) - pas de poids
        right_frame.grid_rowconfigure(4, weight=1)  # Console (row 4)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Éditeur (créé avant la liste des scripts pour le callback on_execute)
        # On passe les callbacks de contrôle (MVC)
        self.editor = ScriptEditor(
            right_frame,
            on_save=self._save_current_script,
            on_run=self._run_current_script,
            on_delete=self._delete_current_script
        )
        self.editor.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Ajouter le bouton thème dans l'en-tête de l'éditeur
        self.theme_button = ttk.Button(
            self.editor.header_buttons,
            text="🎨 Thème",
            command=self._toggle_theme,
            bootstyle="info",
            width=12
        )
        self.editor.add_header_button(self.theme_button)
        
        # === BARRE LATÉRALE GAUCHE ===
        left_frame = ttk.LabelFrame(self, text="")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        left_frame.grid_rowconfigure(4, weight=1)  # Le poids doit être sur la liste (row 4)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Titre de l'application
        title_label = ttk.Label(
            left_frame,
            text="🚀 Script Launcher",
            font=("Segoe UI", 16, "bold"),
            anchor="center"
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=15, padx=15)
        
        # Bouton nouveau script moderne
        new_button = ttk.Button(
            left_frame,
            text="＋ Nouveau script",
            command=self._new_script_dialog,
            bootstyle="success",
            width=25
        )
        new_button.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Séparateur visuel
        separator = ttk.Separator(left_frame, orient="horizontal")
        separator.grid(row=2, column=0, sticky="ew", pady=5)
        
        # Liste des scripts avec titre
        list_label = ttk.Label(
            left_frame,
            text="📜 Scripts disponibles",
            font=("Segoe UI", 10, "bold")
        )
        list_label.grid(row=3, column=0, sticky="w", padx=5, pady=(10, 5))
        
        # Liste des scripts (utilise la méthode du contrôleur via l'éditeur)
        self.script_list = ScriptList(
            left_frame,
            on_select=self._load_script,
            on_execute=self._run_current_script
        )
        self.script_list.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        
        # Afficher le message de bienvenue au démarrage
        self.editor.show_welcome()
        
    def _new_script_dialog(self):
        """Affiche le dialogue de création de script."""
        dialog = ttk.Toplevel(self)
        dialog.title("Nouveau script")
        dialog.transient(self)
        dialog.grab_set()
        dialog.geometry("500x320")
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Formulaire
        ttk.Label(main_frame, text="Nom:", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, padx=5, pady=8, sticky="w")
        name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=name_var).grid(
            row=0, column=1, padx=5, pady=8, sticky="ew"
        )
        
        ttk.Label(main_frame, text="Description:", font=("Segoe UI", 11, "bold")).grid(row=1, column=0, padx=5, pady=8, sticky="w")
        desc_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=desc_var).grid(
            row=1, column=1, padx=5, pady=8, sticky="ew"
        )
        
        ttk.Label(main_frame, text="Auteur:", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, padx=5, pady=8, sticky="w")
        author_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=author_var).grid(
            row=2, column=1, padx=5, pady=8, sticky="ew"
        )
        
        ttk.Label(main_frame, text="Type:", font=("Segoe UI", 11, "bold")).grid(row=3, column=0, padx=5, pady=8, sticky="w")
        type_var = tk.StringVar(value="python")
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=3, column=1, padx=5, pady=8, sticky="w")
        
        ttk.Radiobutton(type_frame, text="Python", variable=type_var, value="python", bootstyle="info").pack(side="left", padx=5)
        ttk.Radiobutton(type_frame, text="Shell", variable=type_var, value="shell", bootstyle="info").pack(side="left", padx=5)
        
        main_frame.grid_columnconfigure(1, weight=1)
        
        def create_script():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror(
                    "Erreur",
                    "Le nom du script est obligatoire."
                )
                return
                
            success = self.script_manager.create_script(
                name=name,
                description=desc_var.get().strip(),
                author=author_var.get().strip(),
                script_type=type_var.get()
            )
            
            if success:
                self._refresh_script_list()
                dialog.destroy()
                self._load_script(name)
            else:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de créer le script '{name}'."
                )
                
        ttk.Button(
            main_frame,
            text="✨ Créer",
            command=create_script,
            bootstyle="success",
            width=20
        ).grid(row=4, column=0, columnspan=2, pady=15)
    
    def _load_scripts_async(self):
        """Charge les scripts de manière asynchrone pour éviter de bloquer l'interface."""
        try:
            # Restaurer explicitement le curseur normal
            self.config(cursor="")
            self.update_idletasks()
            
            # Charger les scripts
            scripts = self.script_manager.get_script_list()
            
            # Mettre à jour la liste avec les types
            self.script_list.update_list(scripts, self._script_types(scripts))
            
            # S'assurer que le curseur reste normal
            self.config(cursor="")
        except Exception as e:
            print(f"Erreur lors du chargement des scripts: {e}")
            self.config(cursor="")
        
    def _refresh_script_list(self):
        """Met à jour la liste des scripts seulement si nécessaire."""
        scripts = self.script_manager.get_script_list()

        self.script_list.update_list(scripts, self._script_types(scripts))

    def _script_types(self, scripts):
        # Récupérer les types de scripts
        script_types = {}
        for script_name in scripts:
            metadata = self.script_manager.get_script_metadata(script_name)
            if metadata:
                script_types[script_name] = metadata.get("type", "python")
        return script_types

    def _load_script(self, script_name: str):
        """Charge un script dans l'éditeur.
        
        Args:
            script_name (str): Nom du script à charger
        """
        if not script_name:
            return
            
        self.current_script = script_name
        self.current_script_original_name = script_name  # Sauvegarder le nom original
        
        try:
            # Charger les métadonnées
            metadata = self.script_manager.get_script_metadata(script_name)
            if not metadata:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de charger les métadonnées de '{script_name}'."
                )
                return
                
            # Charger le code
            code = self.script_manager.get_script_content(script_name)
            if code is None:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de charger le code de '{script_name}'."
                )
                return
                
            # Mettre à jour l'éditeur
            self.editor.set_content(
                name=metadata["name"],
                description=metadata.get("description", ""),
                author=metadata.get("author", ""),
                created=metadata["created_at"],
                modified=metadata["last_modified"],
                executed=metadata.get("last_executed"),
                code=code,
                script_type=metadata.get("type", "python")
            )
            
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Erreur lors du chargement du script '{script_name}': {str(e)}"
            )
    
    # ==================== MÉTHODES DE CONTRÔLE (Controller) ====================
    
    def _save_current_script(self, show_message: bool = True):
        """Enregistre le script courant (Logique métier)."""
        if not self.current_script:
            return
            
        # Récupérer le contenu de l'éditeur (Vue)
        name, description, author, script_type, code = self.editor.get_content()
        
        # Récupérer les métadonnées existantes
        metadata = self.script_manager.get_script_metadata(self.current_script)
        if not metadata:
            messagebox.showerror(
                "Erreur",
                f"Impossible de récupérer les métadonnées de '{self.current_script}'."
            )
            return
            
        # Mettre à jour les métadonnées
        metadata.update({
            "name": name,
            "description": description,
            "author": author,
            "type": script_type
        })
        
        # Vérifier si le nom a changé
        name_changed = (name != self.current_script_original_name)
        
        # Si le nom a changé, renommer d'abord le répertoire
        if name_changed:
            # Vérifier que le nouveau nom n'existe pas déjà
            if name in self.script_manager.get_script_list():
                messagebox.showerror(
                    "Erreur",
                    f"Un script nommé '{name}' existe déjà."
                )
                return
            
            # Renommer le répertoire
            rename_success = self.script_manager.rename_script(self.current_script, name)
            if not rename_success:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de renommer le répertoire de '{self.current_script}' vers '{name}'."
                )
                return
            
            # Mettre à jour le nom courant après le renommage réussi
            self.current_script = name
        
        # Sauvegarder le contenu et les métadonnées
        success = self.script_manager.update_script(
            self.current_script,
            code,
            metadata
        )
        
        if success:
            # Si le nom a changé, mettre à jour l'interface
            if name_changed:
                self.script_list.rename_script(self.current_script_original_name, name)
                self.current_script_original_name = name
                # Rafraîchir la liste complète pour s'assurer de la cohérence
                self._refresh_script_list()
            
            if show_message:
                Messagebox.show_info(
                    title="Succès",
                    message="Script enregistré avec succès."
                )
        else:
            messagebox.showerror(
                "Erreur",
                "Impossible d'enregistrer le script."
            )
    
    def _delete_current_script(self):
        """Supprime le script courant après confirmation (Logique métier)."""
        if not self.current_script:
            messagebox.showwarning(
                "Aucun script sélectionné",
                "Veuillez sélectionner un script à supprimer."
            )
            return
        
        # Demander confirmation avec ttkbootstrap
        confirm = Messagebox.yesno(
            message=f"Êtes-vous sûr de vouloir supprimer le script '{self.current_script}' ?\n\n"
                   "Cette action est irréversible.",
            title="Confirmer la suppression",
            alert=True,
            parent=self
        )
        
        if confirm == "Non":
            return
        
        # Supprimer le script
        success = self.script_manager.delete_script(self.current_script)
        
        if success:
            Messagebox.show_info(
                message=f"Le script '{self.current_script}' a été supprimé avec succès.",
                title="Script supprimé"
            )
            
            # Réinitialiser l'éditeur
            self.current_script = None
            self.current_script_original_name = None
            self.editor.set_content(
                name="",
                description="",
                author="",
                created="",
                modified="",
                executed=None,
                code="",
                script_type="python"
            )
            
            # Vider la console
            self.editor.clear_console()
            
            # Rafraîchir la liste des scripts
            self._refresh_script_list()
        else:
            messagebox.showerror(
                "Erreur",
                f"Impossible de supprimer le script '{self.current_script}'."
            )
    
    def _run_current_script(self, script_name: Optional[str] = None):
        """Enregistre et exécute le script courant dans un thread séparé."""
        # Si un script_name est fourni, on le charge d'abord
        if script_name:
            self._load_script(script_name)
            # Mettre à jour la sélection visuelle dans la liste
            self.script_list._on_select(script_name)
        
        if not self.current_script:
            return
        
        # Sauvegarder le script avant l'exécution (sans afficher de message)
        self._save_current_script(show_message=False)
            
        # Vider la console
        self.editor.clear_console()
        
        # Récupérer le type de script
        metadata = self.script_manager.get_script_metadata(self.current_script)
        script_type = metadata.get("type", "python") if metadata else "python"
        
        # Désactiver le bouton d'exécution
        self.config(cursor="watch")
        self.update_idletasks()
        
        # Fonction exécutée dans le thread
        def run_in_thread():
            try:
                # Exécuter le script
                success = self.executor.execute_script(
                    self.current_script,
                    output_callback=self.editor.console.append,
                    script_type=script_type
                )
                
                # Mettre à jour l'UI dans le thread principal
                self.after(0, lambda: self._on_execution_done(success))
            except Exception as e:
                error_msg = f"\nErreur d'exécution: {str(e)}\n{'='*50}\n"
                self.after(0, lambda: self.editor.console.append(error_msg))
                self.after(0, lambda: self.config(cursor=""))
        
        # Lancer dans un thread daemon
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
    
    def _on_execution_done(self, success: bool):
        """Appelé quand l'exécution du script est terminée."""
        # Restaurer le curseur
        self.config(cursor="")
        
        if success and self.current_script:
            # Mettre à jour la date d'exécution
            self.script_manager.update_execution_time(self.current_script)
            # Recharger le script pour mettre à jour les métadonnées
            self._load_script(self.current_script)
   
    