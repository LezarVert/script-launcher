"""Module contenant le widget ScriptEditor pour éditer les scripts.

Ce module définit la Vue (View) dans le pattern MVC.
Il ne contient aucune logique métier, seulement l'interface utilisateur.
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from typing import Callable, Dict, Optional

from .console_log import ConsoleLog


class ScriptEditor(ttk.Frame):
    """Widget moderne pour éditer un script (Vue).
    
    Cette classe gère uniquement l'affichage et les interactions UI.
    La logique métier est gérée par le contrôleur via des callbacks.
    """
    
    def __init__(
        self, 
        master, 
        on_save: Optional[Callable[[], None]] = None,
        on_run: Optional[Callable[[], None]] = None,
        on_delete: Optional[Callable[[], None]] = None,
        on_mode_change: Optional[Callable[[str], None]] = None,
        icons: Optional[Dict] = None
    ):
        """Initialise l'éditeur de script.
        
        Args:
            master: Widget parent
            on_save: Callback appelé pour sauvegarder le script
            on_run: Callback appelé pour exécuter le script
            on_delete: Callback appelé pour supprimer le script
            on_mode_change: Callback appelé quand le mode change ('welcome' ou 'edit')
            icons: Dictionnaire d'icônes PhotoImage
        """
        super().__init__(master, padding=10)
        
        # Callbacks (fournis par le contrôleur)
        self.on_save_callback = on_save or (lambda: None)
        self.on_run_callback = on_run or (lambda: None)
        self.on_delete_callback = on_delete or (lambda: None)
        self.on_mode_change_callback = on_mode_change
        self.icons = icons or {}
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        # Row 4 (code editor) et Row 6 (console) peuvent s'étendre
        self.grid_rowconfigure(4, weight=1)  # Éditeur de code
        self.grid_rowconfigure(6, weight=1)  # Console
        
        # === EN-TÊTE PRINCIPAL ===
        self.main_header = ttk.Frame(self)
        self.main_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.main_header.grid_columnconfigure(1, weight=1)
        
        # Icône et titre (modifiables)
        self.header_icon = ttk.Label(self.main_header, image=self.icons.get("pencil"))
        self.header_icon.grid(row=0, column=0, padx=(0, 10))
        
        self.header_title = ttk.Label(
            self.main_header, 
            text="Éditeur de script", 
            font=("DejaVu Sans", 12, "bold")
        )
        self.header_title.grid(row=0, column=1, sticky="w")
        
        # Zone pour les boutons personnalisés (à droite)
        self.header_buttons = ttk.Frame(self.main_header)
        self.header_buttons.grid(row=0, column=2, sticky="e")
        
        # === CHAMPS DE MÉTADONNÉES ===
        self.metadata_frame = ttk.Frame(self)
        self.metadata_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.metadata_frame.grid_columnconfigure(2, weight=1)
        
        # Nom
        ttk.Label(
            self.metadata_frame, 
            text="Nom:", 
            font=("DejaVu Sans", 10, "bold")
        ).grid(row=0, column=1, padx=5, pady=5, sticky="e")
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            self.metadata_frame, 
            textvariable=self.name_var, 
            font=("DejaVu Sans", 10)
        )
        self.name_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # Description
        ttk.Label(
            self.metadata_frame, 
            text="Description:", 
            font=("DejaVu Sans", 10, "bold")
        ).grid(row=1, column=1, padx=5, pady=5, sticky="e")
        
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(
            self.metadata_frame, 
            textvariable=self.desc_var, 
            font=("DejaVu Sans", 10)
        )
        self.desc_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        # Auteur
        ttk.Label(
            self.metadata_frame, 
            text="Auteur:", 
            font=("DejaVu Sans", 10, "bold")
        ).grid(row=2, column=1, padx=5, pady=5, sticky="e")
        
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(
            self.metadata_frame, 
            textvariable=self.author_var, 
            font=("DejaVu Sans", 10)
        )
        self.author_entry.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
        
        # Type de script
        ttk.Label(
            self.metadata_frame, 
            text="Type:", 
            font=("DejaVu Sans", 10, "bold")
        ).grid(row=3, column=1, padx=5, pady=5, sticky="e")
        
        self.type_var = tk.StringVar(value="python")
        type_frame = ttk.Frame(self.metadata_frame)
        type_frame.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        ttk.Radiobutton(
            type_frame, 
            image=self.icons.get("python"),
            text="Python",
            compound="left",
            variable=self.type_var, 
            value="python", 
            bootstyle="success"
        ).pack(side="left", padx=5)
        
        ttk.Radiobutton(
            type_frame, 
            image=self.icons.get("shell"),
            text="Shell",
            compound="left",
            variable=self.type_var, 
            value="shell", 
            bootstyle="info"
        ).pack(side="left", padx=5)
        
        # === DATES ===
        self.dates_frame = ttk.Frame(self)
        self.dates_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        self.created_label = ttk.Label(
            self.dates_frame, 
            text=" Créé: -", 
            image=self.icons.get("calendar"),
            compound="left",
            font=("DejaVu Sans", 9)
        )
        self.created_label.pack(side="left", padx=10)
        
        self.modified_label = ttk.Label(
            self.dates_frame, 
            text=" Modifié: -", 
            image=self.icons.get("edit"),
            compound="left",
            font=("DejaVu Sans", 9)
        )
        self.modified_label.pack(side="left", padx=10)
        
        self.executed_label = ttk.Label(
            self.dates_frame, 
            text=" Exécuté: -", 
            image=self.icons.get("played"),
            compound="left",
            font=("DejaVu Sans", 9)
        )
        self.executed_label.pack(side="left", padx=10)
        
        # === ÉDITEUR DE CODE ===
        self.code_header = ttk.Frame(self)
        self.code_header.grid_columnconfigure(1, weight=1)
        
        ttk.Label(
            self.code_header, 
            image=self.icons.get("code")
        ).grid(row=0, column=0, padx=(0, 5))
        
        ttk.Label(
            self.code_header, 
            text="Éditeur de code", 
            font=("DejaVu Sans", 11, "bold")
        ).grid(row=0, column=1, sticky="w")
        
        self.code_frame = ttk.Frame(self)
        self.code_frame.grid_rowconfigure(0, weight=1)
        self.code_frame.grid_columnconfigure(0, weight=1)
        
        # Scrolled Text pour l'éditeur
        self.code_editor = ScrolledText(
            self.code_frame,
            wrap="word",
            height=20,
            font=('Consolas', 11),
            autohide=True,
            bootstyle="primary"
        )
        self.code_editor.grid(row=0, column=0, sticky="nsew")
        
        # === CONSOLE DE SORTIE ===
        self.console_header = ttk.Frame(self)
        
        ttk.Label(
            self.console_header, 
            text=" Console de sortie", 
            image=self.icons.get("terminal"),
            compound="left",
            font=("DejaVu Sans", 12, "bold")
        ).pack(side="left", padx=5)
        
        # Widget console
        self.console = ConsoleLog(self, icons=self.icons)
        
        # === BARRE D'ACTIONS (Boutons Enregistrer, Exécuter, Supprimer) ===
        self.button_frame = ttk.Frame(self)
        # Ne pas gridder ici, sera géré par set_content ou show_welcome
        
        # Boutons avec icônes et style moderne
        btn_save = ttk.Button(
            self.button_frame,
            text=" Enregistrer",
            image=self.icons.get("save"),
            compound="left",
            command=self.on_save_callback,
            bootstyle="primary",
            width=18
        )
        btn_save.pack(side="left", padx=5)
        
        btn_run = ttk.Button(
            self.button_frame,
            text=" Exécuter",
            image=self.icons.get("run"),
            compound="left",
            command=self.on_run_callback,
            bootstyle="success",
            width=18
        )
        btn_run.pack(side="left", padx=5)
        
        btn_delete = ttk.Button(
            self.button_frame,
            text=" Supprimer",
            image=self.icons.get("delete"),
            compound="left",
            command=self.on_delete_callback,
            bootstyle="danger",
            width=18
        )
        btn_delete.pack(side="left", padx=5)
        
        # Masquer le message de bienvenue par défaut
        self.welcome_frame = None
    
    def set_content(
        self, 
        name: str, 
        description: str, 
        author: str,
        created: str, 
        modified: str, 
        executed: Optional[str],
        code: str, 
        script_type: str = "python"
    ):
        """Met à jour le contenu de l'éditeur (Vue)."""
        if not name:
            # Aucun script sélectionné - afficher le message de bienvenue
            self.show_welcome()
            return
        
        # Masquer le message de bienvenue si présent
        if hasattr(self, 'welcome_frame') and self.welcome_frame:
            self.welcome_frame.grid_forget()
        
        # Afficher les champs de métadonnées et l'éditeur
        self.metadata_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.dates_frame.grid(row=2, column=0, sticky="ew", pady=5)
        self.code_header.grid(row=3, column=0, sticky="ew", pady=(10, 5))
        self.code_frame.grid(row=4, column=0, sticky="nsew", pady=(0, 5))
        
        # Afficher la console en bas
        self.console_header.grid(row=5, column=0, sticky="ew", pady=(10, 5))
        self.console.grid(row=6, column=0, sticky="nsew", padx=5, pady=(0, 5))
        
        # Afficher la barre de boutons (row 7, après la console)
        self.button_frame.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
        
        # Remplir les champs
        self.name_var.set(name)
        self.desc_var.set(description)
        self.author_var.set(author)
        self.type_var.set(script_type)
        
        self.created_label.configure(text=f" Créé: {created[:10] if created else '-'}")
        self.modified_label.configure(text=f" Modifié: {modified[:10] if modified else '-'}")
        self.executed_label.configure(
            text=f" Exécuté: {executed[:10] if executed else '-'}"
        )
        
        self.code_editor.delete("1.0", "end")
        self.code_editor.insert("1.0", code)
        self.header_title.configure(text="Métadonnées du script")
        
        # Notifier le changement de mode
        if self.on_mode_change_callback:
            self.on_mode_change_callback('edit')
    
    def show_welcome(self):
        """Affiche le message de bienvenue quand aucun script n'est sélectionné (Vue)."""
        # Masquer les champs de métadonnées et l'éditeur
        self.metadata_frame.grid_remove()
        self.dates_frame.grid_remove()
        self.code_header.grid_remove()
        self.code_frame.grid_remove()
        self.console_header.grid_remove()
        self.console.grid_remove()
        self.button_frame.grid_remove()  # Cacher aussi les boutons d'action
        
        # Créer le frame de bienvenue si nécessaire
        if not hasattr(self, 'welcome_frame') or self.welcome_frame is None:
            self.welcome_frame = ttk.Frame(self)
            self.welcome_frame.grid_columnconfigure(0, weight=1)
            self.welcome_frame.grid_rowconfigure(0, weight=1)
            
            # Frame interne pour centrer
            inner_frame = ttk.Frame(self.welcome_frame)
            inner_frame.grid(row=0, column=0, sticky="nsew")
            
            # Logo fusée
            rocket_label = ttk.Label(
                inner_frame,
                image=self.icons.get("rocket_xl")
            )
            rocket_label.pack(pady=(50, 20))
            
            # Titre
            title_label = ttk.Label(
                inner_frame,
                text="Bienvenue dans Script Launcher",
                font=("DejaVu Sans", 24, "bold")
            )
            title_label.pack(pady=(0, 10))
            
            # Sous-titre
            subtitle_label = ttk.Label(
                inner_frame,
                text="Sélectionnez un script dans la liste ou créez-en un nouveau",
                font=("DejaVu Sans", 12)
            )
            subtitle_label.pack(pady=(0, 50))
        
        self.welcome_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.header_title.configure(text="Bienvenue")
        
        # Notifier le changement de mode
        if self.on_mode_change_callback:
            self.on_mode_change_callback('welcome')
    
    def get_content(self) -> tuple:
        """Récupère le contenu de l'éditeur.
        
        Returns:
            tuple: (nom, description, auteur, type, code)
        """
        return (
            self.name_var.get(),
            self.desc_var.get(),
            self.author_var.get(),
            self.type_var.get(),
            self.code_editor.get("1.0", "end").strip()
        )
    
    def clear_console(self):
        """Vide le contenu de la console (Vue)."""
        self.console.delete("1.0", "end")
    
    def set_header(self, title: str, icon: str = "✎"):
        """Modifie le titre et l'icône de l'en-tête.
        
        Args:
            title (str): Nouveau titre
            icon (str): Nouvelle icône (emoji)
        """
        self.header_title.configure(text=title)
        self.header_icon.configure(text=icon)
    
    def add_header_button(self, widget: tk.Widget):
        """Ajoute un widget (bouton, etc.) dans la zone des boutons de l'en-tête.
        
        Args:
            widget: Le widget à ajouter (doit avoir une méthode pack())
        """
        widget.pack(side="right", padx=5)
    
    def clear_header_buttons(self):
        """Supprime tous les boutons de l'en-tête."""
        for widget in self.header_buttons.winfo_children():
            widget.destroy()
