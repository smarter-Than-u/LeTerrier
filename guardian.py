import os
import re
import subprocess
import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION DYNAMIQUE ---
# Détecte l'utilisateur actuel pour construire le bon chemin
CURRENT_USER = os.getenv("USER") or "fentanylusersarestupid"
TARGET_DIR = f"/home/{CURRENT_USER}/le_terrier"

# Vérification immédiate du répertoire
if not os.path.exists(TARGET_DIR):
    print(f"[-] ERREUR : Le dossier {TARGET_DIR} n'existe pas.")
    print(f"[*] Tentative de repli sur le dossier personnel : {os.path.expanduser('~')}")
    TARGET_DIR = os.path.expanduser("~")

class GuardianHandler(FileSystemEventHandler):
    def __init__(self):
        self.signatures = {
            "XSS Injection": re.compile(r"<script.*?>", re.I),
            "SQL Injection": re.compile(r"UNION SELECT|OR 1=1|--", re.I),
            "Unsafe Execution": re.compile(r"eval\(|exec\(|os\.system\(", re.I)
        }

    def notify(self, attack_type, file_path):
        file_name = os.path.basename(file_path)
        print(f"[!!!] ALERTE : {attack_type} détecté dans {file_name} !")
        
        # Notification visuelle sur le bureau ChromeOS/Linux
        try:
            subprocess.run([
                "notify-send", 
                "OPSA SECURITY ALERT", 
                f"Attack: {attack_type}\nFile: {file_name}", 
                "-u", "critical"
            ])
        except FileNotFoundError:
            pass # notify-send n'est pas installé

    def neutralize(self):
        """ Coupe les accès distants pour expulser les intrus """
        print("[*] ACTION DE DÉFENSE : Verrouillage des services distants...")
        # Coupe le SSH immédiatement
        subprocess.run(["sudo", "systemctl", "stop", "ssh"], stderr=subprocess.DEVNULL)
        # Bloque les connexions entrantes via le pare-feu
        subprocess.run(["sudo", "ufw", "default", "deny", "incoming"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "ufw", "reload"], stderr=subprocess.DEVNULL)
        print("[+] Accès distants coupés. Intrus expulsés.")

    def on_modified(self, event):
        if not event.is_directory:
            try:
                # On attend un court instant que le fichier soit fini d'écrire
                time.sleep(0.1)
                with open(event.src_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for name, pattern in self.signatures.items():
                        if pattern.search(content):
                            self.notify(name, event.src_path)
                            self.neutralize() # ACTIVE LA DÉFENSE
            except Exception as e:
                print(f"[-] Erreur de lecture : {e}")

if __name__ == "__main__":
    print(f"[+] OPSA Guardian activé sur : {TARGET_DIR}")
    print("[+] Surveillance en cours... Appuyez sur Ctrl+C pour arrêter.")
    
    event_handler = GuardianHandler()
    observer = Observer()
    observer.schedule(event_handler, TARGET_DIR, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[!] Guardian désactivé.")
    observer.join()