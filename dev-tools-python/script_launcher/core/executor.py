import os
import subprocess
from typing import Optional, Callable
from datetime import datetime
import time

class ScriptExecutor:
    def __init__(self, base_path: str = "./Scripts"):
        """Initialise l'exécuteur de scripts.
        
        Args:
            base_path (str): Chemin vers le dossier racine des scripts
        """
        self.base_path = os.path.abspath(base_path)
    
    def _get_script_file(self, script_name: str, script_type: str = "python") -> Optional[str]:
        """Détermine le chemin du fichier script selon son type.
        
        Args:
            script_name (str): Nom du script
            script_type (str): Type de script ("python" ou "shell")
            
        Returns:
            Optional[str]: Chemin du fichier ou None si non trouvé
        """
        script_file = "main.sh" if script_type == "shell" else "main.py"
        script_path = os.path.join(self.base_path, script_name, script_file)
        
        if os.path.exists(script_path):
            return script_path
        
        return None
    
    def execute_script(self, script_name: str, output_callback: Optional[Callable[[str], None]] = None, script_type: str = "python") -> bool:
        """Exécute un script et capture sa sortie.
        
        Args:
            script_name (str): Nom du script à exécuter
            output_callback (Optional[Callable[[str], None]]): Fonction appelée pour chaque ligne de sortie
            script_type (str): Type de script ("python" ou "shell")
            
        Returns:
            bool: True si l'exécution a réussi, False sinon
        """
        script_path = self._get_script_file(script_name, script_type)
        log_path = os.path.join(self.base_path, script_name, "log.txt")
        
        if not script_path:
            return False
        
        try:
            # Déterminer la commande à exécuter
            if script_type == "shell":
                command = ["bash", script_path]
            else:
                # Forcer unbuffered pour Python
                command = ["python3", "-u", script_path]
            
            # Ouvrir le fichier de log en mode append
            with open(log_path, "a", encoding="utf-8") as log_file:
                # Écrire l'en-tête d'exécution
                header = f"\n{'='*50}\nExécution du {datetime.now().isoformat()}\nType: {script_type}\n{'='*50}\n"
                log_file.write(header)
                if output_callback:
                    output_callback(header)
                
                # Lancer le script dans un processus séparé
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Capturer la sortie en temps réel
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    
                    if line:
                        log_file.write(line)
                        log_file.flush()
                        if output_callback:
                            output_callback(line)
                
                # Attendre la fin du processus
                return_code = process.wait()
                
                # Écrire le statut de fin
                footer = f"\nStatut de sortie: {'Succès' if return_code == 0 else 'Échec'} (code {return_code})\n{'='*50}\n"
                log_file.write(footer)
                if output_callback:
                    output_callback(footer)
                
                return return_code == 0
                
        except Exception as e:
            error_msg = f"\nErreur d'exécution: {str(e)}\n{'='*50}\n"
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(error_msg)
            if output_callback:
                output_callback(error_msg)
            return False