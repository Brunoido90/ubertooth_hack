📌 Ubertooth Ultimate Toolkit – Übersicht & Setup
Dieses Python-Skript ist ein All-in-One-Tool für Bluetooth- und BLE-Hacking mit einem Ubertooth One (einem speziellen RF-Sniffer). Es bietet eine menübasierte CLI zum Scannen, Sniffen und Angreifen von Bluetooth-Geräten.

📋 Hauptfunktionen
Bluetooth Classic Sniffing (ACL-Daten, Voice Calls)

BLE (Bluetooth Low Energy) Angriffe (Advertisement Sniffing, Follow-Mode)

Custom Attacks (BLE-Spam, Audio-Injection, WiFi/BT-Interferenz)

Spectrum Analyzer (2.4GHz-Frequenzanalyse)

Firmware-Recovery (Ubertooth-Reset)

⚙️ Benötigte Hardware & Module
📌 Hardware
Ubertooth One (oder kompatibles Gerät)

Linux-PC (Kali Linux empfohlen)

📌 Python-Module
bash
pip install colorama pyusb
📌 System-Tools (apt install)
bash
sudo apt install ubertooth libubertooth-dev libbtbb-dev sox hcitool
(Je nach Distro können Paketnamen variieren.)

🔧 Funktionsweise
Root-Check: Läuft nur mit sudo (wegen USB-Zugriff).

Ubertooth-Erkennung: Prüft, ob das Gerät angeschlossen ist.

Interaktives Menü:

Scanning: Findet Bluetooth-/BLE-Geräte in der Nähe.

Sniffing: Fängt Datenverkehr ab (ACL, Voice, BLE).

Jamming: Stört Bluetooth-Kanäle (⚠️ illegal in vielen Ländern!).

Custom Attacks:

BLE-Spam: Erzeugt Fake-Geräte.

Audio-Injection: Spielt Audio auf Zielgeräten ab (theoretisch).

Clean Exit: Beendet alle Prozesse sauber (Strg+C unterstützt).

⚠️ Wichtige Hinweise
Nur für legale Sicherheitstests!

Jamming/Audio-Injection kann strafbar sein!

Nicht alle Funktionen funktionieren mit jedem Bluetooth-Chipset.

🚀 GitHub-ReadMe-Empfehlung
Füge diese Infos in dein README.md ein:

markdown
# Ubertooth Ultimate Toolkit  
All-in-One Bluetooth/BLE Hacking Tool for Ubertooth One  

## 📋 Features  
- Bluetooth Classic & BLE Sniffing  
- Custom Attacks (BLE Spam, Audio Injection)  
- Spectrum Analyzer & Firmware Recovery  

## ⚙️ Installation  
```bash
sudo apt install ubertooth libubertooth-dev libbtbb-dev sox  
pip install colorama pyusb

⚠️ Rechtlicher Haftungsausschluss (Disclaimer) für GitHub
Der folgende Text kann im README.md oder einer separaten LICENSE/DISCLAIMER-Datei eingefügt werden. Er sollte klarstellen, dass der Autor keine Verantwortung für Missbrauch oder Schäden übernimmt:

📜 Haftungsausschluss / Legal Disclaimer
markdown
## ⚠️ Rechtliche Hinweise / Disclaimer  
Der Autor dieses Projekts übernimmt **keine Verantwortung** für die Verwendung dieser Software.  
- Dieses Tool ist **ausschließlich für legale Sicherheitsanalysen und autorisierte Penetrationstests** vorgesehen.  
- **Missbrauch kann strafbar sein** (z. B. unbefugtes Abhören, Störung von Funkverbindungen).  
- Nutzer handeln **auf eigene Verantwortung** und müssen geltende Gesetze (z. B. **FCC, StGB**) beachten.  
- Der Autor distanziert sich ausdrücklich von jeglicher illegaler Nutzung.  

**Nur für Bildungszwecke und ethische Sicherheitsforschung!**  
🔒 Wichtige Punkte für GitHub
Lizenz hinzufügen (z. B. GPLv3/MIT → Klare Nutzungsbedingungen).

Ethik-Hinweis im README (z. B.):

markdown
## 🛡️ Ethische Nutzung  
Dieses Projekt dient der **Cybersecurity-Forschung**.  
- **Erlaubt**: Tests an eigenen Geräten oder mit ausdrücklicher Erlaubnis.  
- **Verboten**: Angriffe auf fremde Systeme ohne Zustimmung.  
Keine Garantie auf Funktionalität/Sicherheit (Standard in Open-Source-Lizenzen).
