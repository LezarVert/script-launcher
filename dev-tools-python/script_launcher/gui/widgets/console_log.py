"""Module contenant le widget ConsoleLog pour afficher la sortie console."""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText


class ConsoleLog(ScrolledText):
    """Widget moderne pour afficher la sortie console."""
    
    def __init__(self, master):
        """Initialise la console.
        
        Args:
            master: Widget parent
        """
        # Créer un Frame avec style moderne
        self.container = ttk.Frame(master, bootstyle="dark")
        
        # En-tête de la console
        header = ttk.Frame(self.container, bootstyle="dark")
        header.pack(fill="x", padx=5, pady=(5, 0))
        
        ttk.Label(
            header, 
            text="💻 Terminal", 
            font=("Segoe UI", 11, "bold"), 
            bootstyle="inverse-dark"
        ).pack(side="left", padx=5)
        
        # Bouton pour vider la console
        self.clear_btn = ttk.Button(
            header,
            text="🗑️",
            command=lambda: self.delete("1.0", "end"),
            bootstyle="dark-outline",
            width=3
        )
        self.clear_btn.pack(side="right", padx=5)
        
        # Zone de texte avec style moderne
        super().__init__(
            self.container,
            wrap="word",
            height=12,
            font=('Consolas', 10),
            state="disabled",
            autohide=True,
            bootstyle="dark"
        )
        self.pack(fill="both", expand=True, padx=5, pady=(0, 5))
    
    def grid(self, **kwargs):
        """Override grid pour appliquer au container."""
        self.container.grid(**kwargs)

    def grid_remove(self):
        """Override grid pour appliquer au container."""
        self.container.grid_remove()

    def grid_forget(self):
        """Override grid pour appliquer au container."""
        self.container.grid_forget()
        
    def append(self, text: str):
        """Ajoute du texte à la console.
        
        Args:
            text (str): Texte à ajouter
        """
        self.text.configure(state="normal")
        self.text.insert("end", text)
        self.text.see("end")
        self.text.configure(state="disabled")
    
    def delete(self, start, end):
        """Supprime du texte de la console.
        
        Args:
            start: Position de début
            end: Position de fin
        """
        self.text.configure(state="normal")
        self.text.delete(start, end)
        self.text.configure(state="disabled")
    
    def configure(self, **kwargs):
        """Configure le widget texte interne."""
        if "state" in kwargs:
            self.text.configure(state=kwargs["state"])
        else:
            super().configure(**kwargs)
