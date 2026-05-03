# Tests de Script Launcher

Ce dossier contient les tests pour le projet Script Launcher.

## Structure

```
tests/
├── __init__.py
├── test_script_manager.py    # Tests pour la gestion des scripts
├── test_executor.py          # Tests pour l'exécution des scripts
├── test_gui.py               # Tests pour l'interface (si applicable)
└── fixtures/                 # Données de test
    └── sample_scripts/
```

## Lancer les tests

```bash
# Installer les dépendances de développement
pip install -e ".[dev]"

# Lancer tous les tests
pytest

# Lancer avec couverture de code
pytest --cov=script_launcher --cov-report=html

# Lancer un fichier de test spécifique
pytest tests/test_script_manager.py -v
```

## Écrire des tests

Nous utilisons `pytest` comme framework de test.

### Exemple de test :

```python
import pytest
from script_launcher.core.script_manager import ScriptManager

def test_create_script():
    """Test la création d'un script."""
    manager = ScriptManager()
    script = manager.create_script("Test", "Description", "python")
    
    assert script is not None
    assert script["name"] == "Test"
    assert script["type"] == "python"
```

## Tests d'intégration vs Tests unitaires

- **Tests unitaires** : Testent une fonction ou classe isolée
- **Tests d'intégration** : Testent l'interaction entre plusieurs composants

## Note sur les tests GUI

Les tests de l'interface graphique sont plus complexes. Nous utilisons `pytest` avec `tkinter` en mode "headless" si possible.

## Contribution

Toute nouvelle fonctionnalité doit inclure des tests. Voir [CONTRIBUTING.md](../CONTRIBUTING.md) pour plus d'informations.
