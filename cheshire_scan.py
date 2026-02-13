import re
import json
import os
import time
from datetime import datetime

# --- La Configuration du Terrier ---
# Copie ton texte Nmap ici
INPUT_TEXT = """[Ton output Nmap ici]"""
SAVE_PATH = "scan_reults.json"

def hatter_notification(message):
    """Envoie une notification système via le terminal Linux."""
    # Utilise 'notify-send' qui est standard sur la plupart des distros Linux
    try:
        os.system(f'notify-send "🎩 Le Chapelier dit:" "{message}"')
    except:
        pass

def existence_vibration():
    """Crée une distorsion visuelle dans le terminal."""
    phrases = [
        "🌀 La réalité est une illusion, le réseau aussi...",
        "🥖 Est-ce que ce port 80 est vraiment libre ou est-ce un rêve ?",
        "🐈 Le chat disparaît, mais les paquets restent.",
        "🍷 Un peu de vin de données, mon ami ?"
    ]
    for phrase in phrases:
        print(f"\t{phrase}")
        time.sleep(0.5)

def enchant_results(text):
    print("🐇 L'entrée dans le terrier de lapin commence...")
    existence_vibration()
    
    # Extraction de l'IP - "Qui es-tu ?" (Style Absolem)
    ip_match = re.search(r"\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)", text)
    target = ip_match.group(1) if ip_match else "Un fantôme numérique"

    # Le Pattern de la Folie
    port_pattern = re.compile(r"(\d+)/tcp\s+open\s+([^\s]+)\s*(.*)")
    hits = port_pattern.findall(text)

    # Construction du Grimoire (JSON)
    grimoire = {
        "manifestation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "the_victim": target,
        "philosophical_state": "Nous sommes tous fous ici",
        "open_doors": []
    }

    for port, service, version in hits:
        ver_info = version.strip() if version else "Une énigme non résolue"
        
        entry = {
            "door_number": int(port),
            "whisper": f"Le service {service} chante '{ver_info}'",
            "threat_level": "Absolument absurde" if "Ubuntu" in ver_info else "Incertain"
        }
        grimoire["open_doors"].append(entry)

    # Sauvegarde des hallucinations
    with open(SAVE_PATH, "w") as f:
        json.dump(grimoire, f, indent=4)
    
    # La notification finale
    message_fin = f"Le scan de {target} est terminé. Le grimoire est prêt, mon ami !"
    print(f"\n✨ {message_fin}")
    hatter_notification(message_fin)

if __name__ == "__main__":
    enchant_results(INPUT_TEXT)