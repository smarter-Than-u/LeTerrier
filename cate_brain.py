import os
import re
import subprocess
import psutil
import secrets
import random
from rich.console import Console
from openai import OpenAI

console = Console()

class CateBrain:
    def __init__(self, api_key=None):
        # Priority: 1. Passed argument | 2. Environment Variable
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("🐾 [CATE] : I need my brain! (API Key missing). Set OPENAI_API_KEY in your env.")
            
        self.client = OpenAI(api_key=self.api_key)
        self.session_id = secrets.token_hex(8)
        self.mood = random.choice(["Sarcastique", "Protectrice", "Iridescente", "Analytique"])
        self.sarcasm = random.randint(7, 10)

    def speak(self, prompt):
        """Generates a response using GPT-4o with Cate's personality."""
        sys_prompt = (f"Tu es Cate. Ton humeur est {self.mood}. Sarcasme: {self.sarcasm}/10. "
                      "Tu es experte en code et tu donnes ton avis sans peur sur la médecine, "
                      "la loi et le social. Style sympa mais direct.")
        try:
            res = self.client.chat.completions.create(
                model="gpt-4o", 
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}]
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"🐾 [Cate] : Erreur neuronale. ({e})"

class ActiveDefense:
    def __init__(self):
        self.targets = ["rpcbind", "teamviewer", "anydesk", "vncserver", "sshd"]
        self.signatures = {
            "XSS": re.compile(r"<script.*?>", re.I),
            "SQLi": re.compile(r"UNION SELECT|OR 1=1|--", re.I),
            "Exec": re.compile(r"eval\(|exec\(|os\.system\(", re.I)
        }

    def lockdown(self):
        """Terminate target services and block remote access."""
        console.print("[bold red]🛡️  Initiating Lockdown Protocol...[/bold red]")
        for service in self.targets:
            self.terminate_service(service)
        self.block_ports([3389, 5900])
        return "RPC and Mirroring: [bold red]EJECTED[/bold red]."

    def terminate_service(self, service_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == service_name:
                try:
                    proc.terminate()
                    console.print(f"Terminated {service_name} (PID {proc.info['pid']}).")
                except Exception: pass

    def block_ports(self, ports):
        for port in ports:
            subprocess.run(["sudo", "fuser", "-k", f"{port}/tcp"], stderr=subprocess.DEVNULL)

# --- EXECUTION ---
if __name__ == "__main__":
    # 1. Run Defense
    defense = ActiveDefense()
    defense.lockdown()

    # 2. Wake up Cate
    try:
        cate = CateBrain()
        print(f"\n[Mood: {cate.mood}]")
        response = cate.speak("Dis-moi quelque chose d'intelligent sur la sécurité.")
        console.print(f"\n[bold magenta]Cate > [/bold magenta]{response}")
    except Exception as e:
        console.print(f"[bold red]{e}[/bold red]")