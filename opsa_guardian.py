import os
import re
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# Change this to the folder you want to protect (e.g., your projects folder)
TARGET_DIR = os.path.expanduser("~/") 

class GuardianHandler(FileSystemEventHandler):
    def __init__(self):
        self.signatures = {
            "XSS Injection": re.compile(r"<script.*?>", re.I),
            "SQL Injection": re.compile(r"UNION SELECT|OR 1=1|--", re.I),
            "Unsafe Execution": re.compile(r"eval\(|exec\(|os\.system\(", re.I)
        }

    def notify(self, attack_type, file_path):
        file_name = os.path.basename(file_path)
        cmd = [
            "notify-send", 
            "OPSA SECURITY ALERT", 
            f"Detected {attack_type} in {file_name}", 
            "-u", "critical"
        ]
        subprocess.run(cmd)

    def on_modified(self, event):
        if not event.is_directory:
            try:
                with open(event.src_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for name, pattern in self.signatures.items():
                        if pattern.search(content):
                            self.notify(name, event.src_path)
            except Exception:
                pass

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(GuardianHandler(), TARGET_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()