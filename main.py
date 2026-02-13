import os
import re
import subprocess
import time
import threading
import secrets
import random
import psutil
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from openai import OpenAI

# --- INITIALISATION ---
console = Console()
USER = os.getenv('USER') or 'fentanylusersarestupid'
BASE_DIR = f"/home/{USER}/le_terrier"

# ============================================================
# MODULE : DÉFENSE ACTIVE (ActiveDefense)
# ============================================================
class ActiveDefense:
    def __init__(self):
        self.targets = ["rpcbind", "teamviewer", "anydesk", "vncserver", "sshd", "chrome-remote-desktop"]
        self.signatures = {
            "XSS": re.compile(r"<script.*?>", re.I),
            "SQLi": re.compile(r"UNION SELECT|OR 1=1|--", re.I),
            "Exec": re.compile(r"eval\(|exec\(|os\.system\(", re.I)
        }

    def lockdown(self):
        """Action immédiate : Termine les services et bloque les ports."""
        console.print("[bold red]🚨 PROTOCOLE DE VERROUILLAGE ACTIVÉ ![/bold red]")
        for service in self.targets:
            self.terminate_service(service)
        self.block_ports([3389, 5900, 22])
        return "[bold green]Défenses actives : Ports et services distants neutralisés.[/bold green]"

    def terminate_service(self, service_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if service_name.lower() in proc.info['name'].lower():
                try:
                    proc.terminate()
                    console.print(f"[bold yellow]💥 Annihilé : {service_name} (PID {proc.info['pid']})[/bold yellow]")
                except: pass

    def block_ports(self, ports):
        for port in ports:
            subprocess.run(["sudo", "fuser", "-k", f"{port}/tcp"], stderr=subprocess.DEVNULL)

# ============================================================
# MODULE : LE CERVEAU DE CATE (CateBrain)
# ============================================================

export OPENAI_API_KEY='ta_cle_api_secrete_ici'
# ============================================================
# MODULE : LA SENTINELLE (Guardian)
# ============================================================
class GuardianHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and any(x in event.src_path for x in [".env", ".py", ".bashrc"]):
            try:
                with open(event.src_path, 'r', errors='ignore') as f:
                    content = f.read()
                    for name, sig in defense.signatures.items():
                        if sig.search(content):
                            console.print(f"\n[bold red]🔥 ALERTE {name} DANS {event.src_path} ![/bold red]")
                            defense.lockdown()
            except: pass

# ============================================================
# INTERFACE PRINCIPALE
# ============================================================
defense = ActiveDefense()

def display_menu():
    os.system('clear')
    console.print(Panel(Text("🍄 OPSA CORE : LE TERRIER 🍄", justify="center", style="bold magenta"), border_style="cyan"))
    
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Code", style="dim", width=6)
    table.add_column("Module", min_width=20)
    table.add_column("Status", justify="right")

    table.add_row("1", "🛡️  Guardian Protocol", "[bold green]ACTIF[/bold green]")
    table.add_row("2", "🐱  Invoquer CATE AI", "[bold magenta]GPT-4 NEURAL[/bold magenta]")
    table.add_row("3", "🌀  Cheshire Scan", "[bold blue]READY[/bold blue]")
    table.add_row("4", "🚪  Quitter", "EXIT")
    
    console.print(table)

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold red]🐾 [CATE] : J'ai besoin de mon cerveau ![/bold red]")
        api_key = console.input("[bold yellow]Entre ta clé OpenAI > [/bold yellow]", password=True)

    cate = CateBrain(api_key)

    if not os.path.exists(BASE_DIR): os.makedirs(BASE_DIR)
    observer = Observer()
    observer.schedule(GuardianHandler(), BASE_DIR, recursive=True)
    observer.start()

    while True:
        display_menu()
        choix = console.input("\n[bold yellow]Que souhaites-tu invoquer ? > [/bold yellow]")

        if choix == "1":
            report = defense.lockdown()
            console.print(report)
            time.sleep(2)
        
        elif choix == "2":
            os.system('clear')
            console.print(Panel(f"Mood: {cate.mood} | Sarcasme: {cate.sarcasm}/10", title="🐾 PORTAIL CATE"))
            while True:
                q = console.input("\n[bold cyan]Toi > [/bold cyan]")
                if q.lower() in ["exit", "back"]: break
                with console.status("[magenta]Cate réfléchit..."):
                    reply = cate.speak(q)
                console.print(f"\n[bold magenta]Cate > [/bold magenta]{reply}")

        elif choix == "3":
            if os.path.exists("cheshire_scan.py"):
                subprocess.run(["python3", "cheshire_scan.py"])
            else:
                console.print("[red]Cheshire Scan introuvable.[/red]")
            input("\nEntrée pour revenir...")

        elif choix == "4":
            observer.stop()
            break

if __name__ == "__main__":
    main()