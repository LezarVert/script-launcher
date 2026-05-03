"""Module contenant le widget ScriptList pour afficher la liste des scripts."""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Callable, Dict, List, Optional


class ScriptList(ttk.Frame):
    """Widget moderne pour afficher la liste des scripts."""
    
    def __init__(
        self, 
        master, 
        on_select: Callable[[str], None], 
        on_execute: Callable[[str], None] = None
    ):
        """Initialise la liste des scripts.
        
        Args:
            master: Widget parent
            on_select: Callback appelé quand un script est sélectionné
            on_execute: Callback appelé quand un script est exécuté
        """
        super().__init__(master, padding=10)
        
        # Initialisation des variables
        self.on_select_callback = on_select
        self.on_execute_callback = on_execute or (lambda x: None)
        self.all_scripts: List[str] = []
        self.script_types: Dict[str, str] = {}  # Stocke le type de chaque script
        self.current_selected = None
        self.script_buttons = {}
        self.last_search = ""
        
        # Configuration du layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Barre de recherche moderne
        search_frame = ttk.Frame(self)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Icône de recherche
        search_icon = ttk.Label(search_frame, text="🔍", font=("Segoe UI", 12))
        search_icon.grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bootstyle="primary"
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Placeholder
        self.placeholder = "Rechercher un script..."
        self.is_placeholder = True
        self.search_entry.insert(0, self.placeholder)
        self.search_entry.config(foreground="gray")
        
        def on_focus_in(e):
            if self.is_placeholder:
                self.search_entry.delete(0, "end")
                # self.search_entry.config(foreground="white")
                self.is_placeholder = False
        
        def on_focus_out(e):
            if not self.search_entry.get():
                self.is_placeholder = True
                self.search_entry.insert(0, self.placeholder)
                self.search_entry.config(foreground="gray")
                self.last_search = ""
                self._show_all_scripts()
        
        self.search_entry.bind("<FocusIn>", on_focus_in)
        self.search_entry.bind("<FocusOut>", on_focus_out)
        
        # Compteur de scripts
        self.counter_label = ttk.Label(
            self,
            text="0 script(s)",
            font=("Segoe UI", 9)
        )
        self.counter_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        # Frame avec canvas pour la liste scrollable
        list_container = ttk.Frame(self)
        list_container.grid(row=2, column=0, sticky="nsew", pady=(0, 5))
        list_container.grid_rowconfigure(0, weight=1)
        list_container.grid_columnconfigure(0, weight=1)
        
        # Canvas et scrollbar modernes
        self.canvas = tk.Canvas(list_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, command=self.canvas.yview)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 2), pady=2)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=2)
        
        # Frame pour les boutons
        self.scrollable_frame = ttk.Frame(self.canvas)
        canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Mise à jour du scroll
        def configure_scroll(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        def configure_canvas(event):
            canvas_width = event.width
            self.canvas.itemconfig(canvas_window, width=canvas_width)
        
        self.scrollable_frame.bind("<Configure>", configure_scroll)
        self.canvas.bind("<Configure>", configure_canvas)

        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-4>", lambda e: self._on_mousewheel(type('', (), {'delta': 120})()))
        self.scrollable_frame.bind("<Button-5>", lambda e: self._on_mousewheel(type('', (), {'delta': -120})()))
        
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", lambda e: self._on_mousewheel(type('', (), {'delta': 120})()))
        self.canvas.bind("<Button-5>", lambda e: self._on_mousewheel(type('', (), {'delta': -120})()))

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.search_var.trace_add("write", self._on_search_changed)
    
    def _on_mousewheel(self, event):
        bbox = self.canvas.bbox("all")
        if bbox:
            canvas_height = self.canvas.winfo_height()
            content_height = bbox[3] - bbox[1]
            if content_height > canvas_height:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_search_changed(self, *args):
        """Filtre la liste seulement si le texte a vraiment changé."""
        # Ignorer si c'est le placeholder
        if self.is_placeholder:
            return
        
        search_text = self.search_var.get().strip().lower()
        
        # Éviter les rafraîchissements inutiles
        if search_text == self.last_search:
            return
        
        self.last_search = search_text
        
        # Si vide, afficher tous les scripts
        if not search_text:
            self._show_all_scripts()
            return
        
        # Filtrer efficacement sans recréer tous les boutons
        if self.script_buttons:  # Vérifier que les boutons existent
            for script_name, (container, left_btn, right_btn) in list(self.script_buttons.items()):
                if search_text in script_name.lower():
                    container.pack(fill="x", pady=2)
                else:
                    container.pack_forget()
    
    def _clear_buttons(self):
        """Efface tous les boutons."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.script_buttons.clear()
    
    def _create_button(self, script_name: str, script_type: str = "python"):
        """Crée un bouton moderne pour un script."""
        # Frame contenant le bouton avec style moderne
        btn_container = ttk.Frame(self.scrollable_frame)
        btn_container.grid_columnconfigure(0, weight=1)
        btn_container.pack(fill="x", pady=3, padx=2)
        
        # Icône selon le type
        type_icon = "🐍" if script_type == "python" else "🐚"
        
        # Bouton principal avec icône
        left_btn = ttk.Button(
            btn_container,
            text=f"{type_icon} {script_name}",
            command=lambda s=script_name: self._on_select(s),
            bootstyle="success",
            width=28,
            padding=(10, 8)
        )
        left_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Bouton d'exécution rapide
        right_btn = ttk.Button(
            btn_container,
            text="▶",
            command=lambda s=script_name: self.on_execute_callback(s),
            bootstyle="success",
            width=4,
            padding=(5, 8)
        )
        right_btn.grid(row=0, column=1, sticky="e")


        widgets_to_bind = [btn_container, left_btn, right_btn]
        for widget in widgets_to_bind:
            widget.bind("<MouseWheel>", lambda e: self._on_mousewheel(e))
            widget.bind("<Button-4>", lambda e: self._on_mousewheel(type('', (), {'delta': 120})()))
            widget.bind("<Button-5>", lambda e: self._on_mousewheel(type('', (), {'delta': -120})()))
        
        self.script_buttons[script_name] = (btn_container, left_btn, right_btn)
    
    def _show_all_scripts(self):
        """Affiche tous les scripts sans recréer les boutons."""
        if self.script_buttons:  # Vérifier que les boutons existent
            for script_name, (container, left_btn, right_btn) in self.script_buttons.items():
                container.pack(fill="x", pady=3)
            self._highlight_selected()
    
    def _on_select(self, script_name: str):
        """Sélectionne un script."""
        self.current_selected = script_name
        self._highlight_selected()
        self.on_select_callback(script_name)
    
    def _highlight_selected(self):
        """Met en évidence le script sélectionné."""
        for script_name, (container, left_btn, right_btn) in self.script_buttons.items():
            if script_name == self.current_selected:
                left_btn.configure(bootstyle="primary")
            else:
                left_btn.configure(bootstyle="secondary")
    
    def update_list(self, scripts: List[str], script_types: Optional[Dict[str, str]] = None):
        """Met à jour la liste des scripts seulement si elle a changé.
        
        Args:
            scripts (List[str]): Liste des noms de scripts
            script_types (Optional[Dict[str, str]]): Dictionnaire des types de scripts
        """
        # Vérifier si la liste a réellement changé
        if set(scripts) == set(self.all_scripts):
            return
        
        self.all_scripts = scripts
        self.last_search = ""  # Réinitialiser la recherche
        
        # Mettre à jour les types
        if script_types:
            self.script_types = script_types
        else:
            self.script_types = {script: "python" for script in scripts}
        
        # Mettre à jour le compteur
        self.counter_label.configure(text=f"{len(scripts)} script(s)")
        
        # Recréer tous les boutons
        self._clear_buttons()
        for script in self.all_scripts:
            script_type = self.script_types.get(script, "python")
            self._create_button(script, script_type)
        self._highlight_selected()
    
    def rename_script(self, old_name: str, new_name: str):
        """Renomme un script sans rafraîchir toute la liste.
        
        Args:
            old_name (str): Ancien nom
            new_name (str): Nouveau nom
        """
        if old_name in self.all_scripts:
            idx = self.all_scripts.index(old_name)
            self.all_scripts[idx] = new_name
            if old_name == self.current_selected:
                self.current_selected = new_name
            
            # Mettre à jour le type
            if old_name in self.script_types:
                self.script_types[new_name] = self.script_types.pop(old_name)
            
            # Mettre à jour seulement le bouton concerné
            if old_name in self.script_buttons:
                container, left_btn, right_btn = self.script_buttons[old_name]
                script_type = self.script_types.get(new_name, "python")
                type_icon = "🐍" if script_type == "python" else "🐚"
                left_btn.configure(text=f"{type_icon} {new_name}")
                left_btn.configure(command=lambda s=new_name: self._on_select(s))
                right_btn.configure(command=lambda s=new_name: self.on_execute_callback(s))
                self.script_buttons[new_name] = self.script_buttons.pop(old_name)
