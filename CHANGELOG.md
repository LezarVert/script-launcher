# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

### Ajouté
- Documentation complète pour l'open source
- Fichiers de contribution (CONTRIBUTING.md, CODE_OF_CONDUCT.md)
- Templates d'issues GitHub
- Licence MIT

### Modifié
- Nettoyage des anciens fichiers markdown
- Mise à jour du README principal

## [1.0.0] - 2026-05-03

### Ajouté
- Interface graphique moderne avec ttkbootstrap
- Gestion complète des scripts (CRUD)
- Support des scripts Python et Shell
- Thèmes multiples (darkly, superhero, solar, flatly)
- Éditeur de code intégré
- Console de sortie en temps réel
- Barre de recherche avec filtrage
- Raccourcis clavier (Ctrl+S, F5, Ctrl+F, Ctrl+N, Ctrl+Q)
- Métadonnées des scripts (nom, description, auteur, dates)
- Historique d'exécution
- Compilation avec PyInstaller
- Fichier de configuration des préférences
- Intégration système Linux (.desktop)

### Technique
- Architecture MVC (Model-View-Controller)
- Utilisation de threading pour l'exécution non-bloquante
- Gestion des imports cachés PyInstaller (PIL._tkinter_finder)
- Logging système

---

## Types de changements
- `Ajouté` pour les nouvelles fonctionnalités
- `Modifié` pour les changements de fonctionnalités existantes
- `Déprécié` pour fonctionnalités qui seront bientôt supprimées
- `Supprimé` pour fonctionnalités supprimées
- `Corrigé` pour les corrections de bugs
- `Sécurité` en cas de vulnérabilités
