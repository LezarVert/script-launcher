# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à **Script Launcher** ! Ce document vous guidera dans le processus de contribution.

## 📋 Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment puis-je contribuer ?](#comment-puis-je-contribuer-)
- [Pull Requests](#pull-requests)
- [Standards de code](#standards-de-code)
- [Signaler des bugs](#signaler-des-bugs)

## 📜 Code de conduite

En participant à ce projet, vous acceptez de respecter notre [Code de Conduite](CODE_OF_CONDUCT.md). Veuillez le lire pour comprendre ce qui est attendu.

## 🎯 Comment puis-je contribuer ?

### 🐛 Signaler des bugs

Les bugs sont suivis via [GitHub Issues](https://github.com/LezarVert/script-launcher/issues).

**Avant de créer une issue :**
- Vérifiez que le bug n'a pas déjà été signalé
- Utilisez un titre clair et descriptif
- Incluez les informations suivantes :
  - Votre système d'exploitation (Windows, Linux, macOS)
  - Version de Python
  - Étapes pour reproduire le bug
  - Comportement attendu vs comportement observé
  - Captures d'écran si applicable

### 💡 Suggérer des améliorations

Les suggestions sont également les bienvenues ! Ouvrez une issue avec le label `enhancement`.

### 🔧 Pull Requests

1. **Fork** le projet
2. **Clone** votre fork :
   ```bash
   git clone https://github.com/LezarVert/script-launcher.git
   ```
3. **Créez une branche** pour votre fonctionnalité :
   ```bash
   git checkout -b feature/AmazingFeature
   ```
4. **Développez** votre fonctionnalité :
   - Suivez les standards de code (voir ci-dessous)
   - Ajoutez des tests si applicable
   - Mettez à jour la documentation si nécessaire
5. **Commit** vos changements :
   ```bash
   git commit -m 'feat: add AmazingFeature'
   ```
6. **Push** vers votre fork :
   ```bash
   git push origin feature/AmazingFeature
   ```
7. **Ouvrez une Pull Request** vers la branche `main`

## 📏 Standards de code

### Python
- Respectez **PEP 8**
- Utilisez des **type hints**
- Documentez avec des **docstrings** (Google style)
- Utilisez des **virtual environments**

### Structure du code
- Respectez l'architecture **MVC**
- Gardez les fonctions courtes et focussées
- Utilisez des noms de variables explicites

### Exemple de fonction bien documentée :
```python
def create_script(name: str, description: str, script_type: str) -> dict:
    """
    Crée un nouveau script avec ses métadonnées.
    
    Args:
        name: Nom du script
        description: Description du script
        script_type: Type de script ('python' ou 'shell')
        
    Returns:
        dict: Métadonnées du script créé
        
    Raises:
        ValueError: Si le type de script est invalide
    """
    pass
```

### Messages de commit
Utilisez la convention [Conventional Commits](https://www.conventionalcommits.org/) :

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` documentation
- `style:` formatage, pas de changement de code
- `refactor:` refactoring du code
- `test:` ajout ou modification de tests
- `chore:` tâches diverses (build, tools, etc.)

## 🧪 Tests

Bien que le projet n'ait pas encore de tests automatisés complets, les contributions incluant des tests sont encouragées !

```bash
# Lancer les tests (quand ils seront disponibles)
pytest tests/
```

## 📚 Documentation

- Mettez à jour le README.md si nécessaire
- Documentez les nouvelles fonctionnalités
- Ajoutez des docstrings au code

## ❓ Questions ?

N'hésitez pas à ouvrir une issue avec le label `question` si vous avez besoin d'aide !

---

**Merci de contribuer à Script Launcher ! 🚀**
