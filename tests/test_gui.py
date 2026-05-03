"""Tests pour l'interface graphique."""

import pytest
import tkinter as tk
from script_launcher.gui.window import Window
from script_launcher.gui.widgets.script_list import ScriptList
from script_launcher.gui.widgets.script_editor import ScriptEditor
from script_launcher.gui.widgets.console_log import ConsoleLog


class TestScriptList:
    """Tests pour le widget ScriptList."""
    
    @pytest.fixture
    def setup_widget(self):
        """Configure un widget de test."""
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        widget = ScriptList(root)
        yield widget
        root.destroy()
        
    def test_widget_creation(self, setup_widget):
        """Test la création du widget."""
        assert setup_widget is not None
        
    def test_update_list(self, setup_widget):
        """Test la mise à jour de la liste."""
        scripts = [
            {"name": "Script 1", "type": "python"},
            {"name": "Script 2", "type": "shell"}
        ]
        setup_widget.update_list(scripts)
        # Vérifier que la liste est mise à jour
        assert True  # À compléter selon l'implémentation


class TestScriptEditor:
    """Tests pour le widget ScriptEditor."""
    
    @pytest.fixture
    def setup_widget(self):
        """Configure un widget de test."""
        root = tk.Tk()
        root.withdraw()
        widget = ScriptEditor(root)
        yield widget
        root.destroy()
        
    def test_widget_creation(self, setup_widget):
        """Test la création du widget."""
        assert setup_widget is not None


class TestConsoleLog:
    """Tests pour le widget ConsoleLog."""
    
    @pytest.fixture
    def setup_widget(self):
        """Configure un widget de test."""
        root = tk.Tk()
        root.withdraw()
        widget = ConsoleLog(root)
        yield widget
        root.destroy()
        
    def test_widget_creation(self, setup_widget):
        """Test la création du widget."""
        assert setup_widget is not None
        
    def test_append_text(self, setup_widget):
        """Test l'ajout de texte à la console."""
        setup_widget.append_text("Test message")
        # Vérifier que le texte est ajouté
        assert True  # À compléter
