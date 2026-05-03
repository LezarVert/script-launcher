import os
import json
from datetime import datetime
from typing import Dict, Optional, List

class ScriptManager:
    def __init__(self, base_path: str = "./Scripts"):
        """Initialise le gestionnaire de scripts.
        
        Args:
            base_path (str): Chemin vers le dossier racine des scripts
        """
        self.base_path = os.path.abspath(base_path)
        self._ensure_base_directory()
    
    def _ensure_base_directory(self) -> None:
        """Crée le dossier de base s'il n'existe pas."""
        os.makedirs(self.base_path, exist_ok=True)
    
    def create_script(self, name: str, description: str = "", author: str = "", initial_code: str = "", script_type: str = "python") -> bool:
        """Crée un nouveau script avec ses métadonnées.
        
        Args:
            name (str): Nom du script (et du dossier)
            description (str): Description du script
            author (str): Auteur du script
            initial_code (str): Code initial du script
            script_type (str): Type de script ("python" ou "shell")
            
        Returns:
            bool: True si la création a réussi, False sinon
        """
        script_path = os.path.join(self.base_path, name)
        
        # Vérifier si le script existe déjà
        if os.path.exists(script_path):
            return False
            
        try:
            # Créer le dossier du script
            os.makedirs(script_path)
            
            # Déterminer l'extension et le shebang en fonction du type
            if script_type == "shell":
                script_file = "main.sh"
                if not initial_code.startswith("#!"):
                    initial_code = "#!/bin/bash\n\n" + initial_code
            else:  # python par défaut
                script_file = "main.py"
                if not initial_code.startswith("#!"):
                    initial_code = "#!/usr/bin/env python3\n\n" + initial_code
            
            # Créer le fichier main.{sh|py}
            with open(os.path.join(script_path, script_file), "w", encoding="utf-8") as f:
                f.write(initial_code)
            
            # Rendre le fichier exécutable
            os.chmod(os.path.join(script_path, script_file), 0o755)
            
            # Créer le fichier log.txt vide
            with open(os.path.join(script_path, "log.txt"), "w", encoding="utf-8") as f:
                pass
            
            # Créer le fichier meta.json
            metadata = {
                "name": name,
                "description": description,
                "author": author,
                "type": script_type,
                "created_at": datetime.now().isoformat(),
                "last_executed": None,
                "last_modified": datetime.now().isoformat()
            }
            
            with open(os.path.join(script_path, "meta.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Erreur lors de la création du script: {e}")
            return False
    
    def get_script_list(self) -> List[str]:
        """Retourne la liste des scripts disponibles.
        
        Returns:
            List[str]: Liste des noms de scripts
        """
        if not os.path.exists(self.base_path):
            return []
            
        return [d for d in os.listdir(self.base_path) 
                if os.path.isdir(os.path.join(self.base_path, d))]
    
    def get_script_metadata(self, script_name: str) -> Optional[Dict]:
        """Récupère les métadonnées d'un script.
        
        Args:
            script_name (str): Nom du script
            
        Returns:
            Optional[Dict]: Métadonnées du script ou None si non trouvé
        """
        meta_path = os.path.join(self.base_path, script_name, "meta.json")
        
        if not os.path.exists(meta_path):
            return None
            
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    
    def get_script_content(self, script_name: str) -> Optional[str]:
        """Récupère le contenu du script.
        
        Args:
            script_name (str): Nom du script
            
        Returns:
            Optional[str]: Contenu du script ou None si non trouvé
        """
        metadata = self.get_script_metadata(script_name)
        if not metadata:
            return None
        
        script_type = metadata.get("type", "python")
        script_file = "main.sh" if script_type == "shell" else "main.py"
        script_path = os.path.join(self.base_path, script_name, script_file)
        
        if not os.path.exists(script_path):
            return None
            
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None
    
    def update_script(self, script_name: str, code: str, metadata: Dict) -> bool:
        """Met à jour un script et ses métadonnées.
        
        Args:
            script_name (str): Nom du script
            code (str): Nouveau contenu du script
            metadata (Dict): Nouvelles métadonnées
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        script_dir = os.path.join(self.base_path, script_name)
        
        if not os.path.exists(script_dir):
            return False
            
        try:
            # Déterminer le type de script
            script_type = metadata.get("type", "python")
            old_metadata = self.get_script_metadata(script_name)
            old_type = old_metadata.get("type", "python") if old_metadata else "python"
            
            # Si le type a changé, supprimer l'ancien fichier
            if old_type != script_type:
                old_file = "main.sh" if old_type == "shell" else "main.py"
                old_path = os.path.join(script_dir, old_file)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # Déterminer le nouveau nom de fichier
            script_file = "main.sh" if script_type == "shell" else "main.py"
            script_path = os.path.join(script_dir, script_file)
            
            # Mise à jour du code
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            # Rendre le fichier exécutable
            os.chmod(script_path, 0o755)
            
            # Mise à jour des métadonnées
            metadata["last_modified"] = datetime.now().isoformat()
            with open(os.path.join(script_dir, "meta.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour du script: {e}")
            return False
    
    def update_execution_time(self, script_name: str) -> bool:
        """Met à jour la date de dernière exécution d'un script.
        
        Args:
            script_name (str): Nom du script
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        metadata = self.get_script_metadata(script_name)
        if metadata is None:
            return False
            
        metadata["last_executed"] = datetime.now().isoformat()
        
        meta_path = os.path.join(self.base_path, script_name, "meta.json")
        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4)
            return True
        except Exception:
            return False
    
    def rename_script(self, old_name: str, new_name: str) -> bool:
        """Renomme un script et son répertoire.
        
        Args:
            old_name (str): Ancien nom du script
            new_name (str): Nouveau nom du script
            
        Returns:
            bool: True si le renommage a réussi, False sinon
        """
        old_dir = os.path.join(self.base_path, old_name)
        new_dir = os.path.join(self.base_path, new_name)
        
        # Vérifier que l'ancien répertoire existe
        if not os.path.exists(old_dir):
            return False
        
        # Vérifier que le nouveau nom n'existe pas déjà
        if os.path.exists(new_dir):
            return False
        
        try:
            # Renommer le répertoire
            os.rename(old_dir, new_dir)
            return True
        except Exception as e:
            print(f"Erreur lors du renommage du script: {e}")
            return False
    
    def delete_script(self, script_name: str) -> bool:
        """Supprime un script et tous ses fichiers.
        
        Args:
            script_name (str): Nom du script à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        script_dir = os.path.join(self.base_path, script_name)
        
        if not os.path.exists(script_dir):
            return False
        
        try:
            import shutil
            shutil.rmtree(script_dir)
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du script: {e}")
            return False
