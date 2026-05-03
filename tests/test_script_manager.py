"""Tests pour le gestionnaire de scripts."""

import pytest
import json
import os
import tempfile
from pathlib import Path

from script_launcher.core.script_manager import ScriptManager


@pytest.fixture
def temp_scripts_dir():
    """Crée un dossier temporaire pour les tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def script_manager(temp_scripts_dir):
    """Initialise un ScriptManager avec un dossier temporaire."""
    return ScriptManager(scripts_dir=temp_scripts_dir)


class TestScriptManager:
    """Tests pour la classe ScriptManager."""
    
    def test_create_python_script(self, script_manager, temp_scripts_dir):
        """Test la création d'un script Python."""
        script = script_manager.create_script(
            name="Test Script",
            description="Un script de test",
            author="Test Author",
            script_type="python"
        )
        
        assert script["name"] == "Test Script"
        assert script["type"] == "python"
        assert os.path.exists(os.path.join(temp_scripts_dir, script["folder"], "main.py"))
        
    def test_create_shell_script(self, script_manager, temp_scripts_dir):
        """Test la création d'un script Shell."""
        script = script_manager.create_script(
            name="Test Shell",
            description="Un script shell",
            author="Test Author",
            script_type="shell"
        )
        
        assert script["type"] == "shell"
        assert os.path.exists(os.path.join(temp_scripts_dir, script["folder"], "main.sh"))
        
    def test_delete_script(self, script_manager, temp_scripts_dir):
        """Test la suppression d'un script."""
        script = script_manager.create_script("To Delete", "Test", "python")
        script_path = os.path.join(temp_scripts_dir, script["folder"])
        
        assert os.path.exists(script_path)
        
        result = script_manager.delete_script(script["folder"])
        
        assert result is True
        assert not os.path.exists(script_path)
        
    def test_list_scripts(self, script_manager):
        """Test le listage des scripts."""
        script_manager.create_script("Script 1", "Desc 1", "python")
        script_manager.create_script("Script 2", "Desc 2", "shell")
        
        scripts = script_manager.list_scripts()
        
        assert len(scripts) == 2
        
    def test_rename_script(self, script_manager, temp_scripts_dir):
        """Test le renommage d'un script."""
        script = script_manager.create_script("Old Name", "Desc", "python")
        old_folder = script["folder"]
        
        result = script_manager.rename_script(old_folder, "New Name")
        
        assert result is True
        assert os.path.exists(os.path.join(temp_scripts_dir, "New_Name"))
        assert not os.path.exists(os.path.join(temp_scripts_dir, old_folder))
