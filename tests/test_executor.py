"""Tests pour l'exécuteur de scripts."""

import pytest
import tempfile
import os
from script_launcher.core.executor import ScriptExecutor


@pytest.fixture
def executor():
    """Initialise un ScriptExecutor."""
    return ScriptExecutor()


@pytest.fixture
def temp_script():
    """Crée un script temporaire pour les tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "test_script.py")
        with open(script_path, "w") as f:
            f.write('print("Hello from test script!")\n')
        
        # Créer le meta.json
        meta = {
            "name": "Test Script",
            "type": "python"
        }
        with open(os.path.join(tmpdir, "meta.json"), "w") as f:
            import json
            json.dump(meta, f)
            
        yield tmpdir


class TestScriptExecutor:
    """Tests pour la classe ScriptExecutor."""
    
    def test_execute_python_script(self, executor, temp_script):
        """Test l'exécution d'un script Python."""
        output = []
        result = executor.execute(
            script_path=os.path.join(temp_script, "main.py"),
            script_type="python",
            callback=lambda line: output.append(line)
        )
        
        assert result["returncode"] == 0
        assert len(output) > 0
        
    def test_execute_nonexistent_script(self, executor):
        """Test l'exécution d'un script inexistant."""
        result = executor.execute(
            script_path="/nonexistent/script.py",
            script_type="python"
        )
        
        assert result["returncode"] != 0
