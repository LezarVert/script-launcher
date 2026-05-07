#!/usr/bin/env python3
"""Sauvegarde simple des fichiers de configuration"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# ========== CONFIGURATION ==========
SOURCE_DIR = os.path.expanduser('~/VSCode')          # Répertoire à sauvegarder
BACKUP_DIR = os.path.expanduser('~/EnvBackup')   # Défaut: SaveEnv/backups. Sinon : os.path.expanduser('/path/to/backup')
IGNORE_DIRS = [
    'node_modules', '__pycache__', '.git', '.venv', 'venv',
    'dist', 'build', 'target', '.gradle', 'vendor'
]

# Fichiers de configuration à sauvegarder
CONFIG_PATTERNS = {
    'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'requirements.txt', 'Pipfile', 'Pipfile.lock', 'pyproject.toml', 'poetry.lock',
    'composer.json', 'composer.lock', 'pom.xml', 'build.gradle', 'gradle.properties',
    '.env', '.gitignore', '.editorconfig', 'tsconfig.json', 'Dockerfile', 'docker-compose.yml',
    'Makefile', 'nuxt.config.js', 'nuxt.config.ts', 'setup.py', '.nvmrc', '.python-version',
}
# ===================================

class ConfigBackup:

    def __init__(self, source_dir: str = None):
        self.source_dir = Path(source_dir or SOURCE_DIR).resolve()
        
        if BACKUP_DIR:
            self.backup_dir = Path(BACKUP_DIR).resolve()
        else:
            self.backup_dir = Path(__file__).parent / 'backups'
        
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = self.backup_dir / f'config_backup_{timestamp}'
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
        self.total_files = 0
        self.total_size = 0

    def should_backup(self, file_path: Path) -> bool:
        """Vérifie si un fichier doit être sauvegardé"""
        return file_path.name in CONFIG_PATTERNS or file_path.name.startswith('.env')

    def scan_and_backup(self):
        """Scanne et sauvegarde les fichiers"""
        print(f"📂 Scan: {self.source_dir}")
        print(f"💾 Destination: {self.backup_path}\n")

        for root, dirs, files in os.walk(self.source_dir):
            # Ignorer les dossiers volumineux
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file_name in files:
                file_path = Path(root) / file_name
                if self.should_backup(file_path):
                    self._backup_file(file_path)

    def _backup_file(self, file_path: Path):
        """Sauvegarde un fichier"""
        try:
            relative_path = file_path.relative_to(self.source_dir)
            dest_path = self.backup_path / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest_path)
            
            size = file_path.stat().st_size
            self.total_files += 1
            self.total_size += size
            
            print(f"✓ {relative_path} ({self._format_size(size)})")
        except Exception as e:
            print(f"✗ {file_path}: {e}")

    def compress(self):
        """Compresse en ZIP"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_path = self.backup_dir / f'config_backup_{timestamp}.zip'
        
        print(f"\n📦 Compression...")
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.backup_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.backup_dir)
                    zipf.write(file_path, arcname)
        
        size = archive_path.stat().st_size
        print(f"✓ Archive: {archive_path.name} ({self._format_size(size)})")
        
        # Supprimer le dossier non compressé
        shutil.rmtree(self.backup_path)

    def report(self):
        """Affiche un rapport"""
        print("\n" + "="*60)
        print(f"✅ Sauvegarde terminée!")
        print("="*60)
        print(f"Fichiers: {self.total_files}")
        print(f"Taille: {self._format_size(self.total_size)}")
        print(f"📍 Backups: {self.backup_dir}")
        print("="*60)

    @staticmethod
    def _format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def run(self):
        """Lance le backup complet"""
        self.scan_and_backup()
        self.compress()
        self.report()


if __name__ == '__main__':
    import sys
    source = sys.argv[1] if len(sys.argv) > 1 else None
    backup = ConfigBackup(source)
    backup.run()