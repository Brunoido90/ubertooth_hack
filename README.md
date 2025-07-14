Ubertooth One Evil Toolkit 🔥📻
Ein mächtiges Python-Toolkit für Bluetooth-Angriffe mit dem Ubertooth One, inklusive Live-Audio-Hijacking, MP3-Injection und Jamming-Funktionen. Entwickelt für Sicherheitsforschung und pentesting.

📥 Installation
Voraussetzungen
Hardware: Ubertooth One

Betriebssystem: Linux (getestet auf Kali Linux, Ubuntu)

Python: 3.6+

Root-Zugriff erforderlich

1. Abhängigkeiten installieren
bash
# Installiere notwendige System-Tools
sudo apt update
sudo apt install -y \
    ubertooth \
    bluez \
    sox \
    libsox-fmt-mp3 \
    python3-pip \
    git

# Python-Module
pip3 install colorama
2. Tool herunterladen
bash
git clone https://github.com/deinusername/ubertooth-evil-toolkit.git
cd ubertooth-evil-toolkit
chmod +x uber_evil.py
3. Ausführen
bash
sudo python3 uber_evil.py
🔧 Funktionsübersicht
Funktion	Beschreibung
Bluetooth-Scanning	Findet alle sichtbaren Bluetooth- und BLE-Geräte in Reichweite.
Live-Audio-Hijack	Hört Gespräche über Bluetooth-Headsets in Echtzeit ab und zeichnet sie auf.
MP3-Injection	Spielt eine eigene MP3-Datei auf dem Zielgerät ab (HSP/HFP).
Channel-Jamming	Stört gezielt Bluetooth- oder WiFi-Kanäle (DoS).
Firmware-Flash	Flasht die Firmware des Ubertooth (Notfall-Reset).
⚡ Verwendung
Geräte scannen

bash
sudo python3 uber_evil.py
Wähle Option 1 zum Scannen.

Live-Audio abhören

Wähle ein Zielgerät aus der Liste.

Wähle "Live Audio Hijack" (Option 1).

Die Aufnahme wird automatisch als .wav gespeichert.

MP3-Datei injizieren

Wähle "Inject MP3 to Target" (Option 2).

Gib die BD_ADDR des Ziels ein (z. B. 01:23:45:67:89:AB).

Wähle eine MP3-Datei aus.

Das Zielgerät spielt jetzt deine Audio ab!

Bluetooth stören (Jamming)

Wähle "Channel Jamming" (Option 3).

Bestätige mit Enter, um den Angriff zu stoppen.

⚠️ Rechtlicher Hinweis
❌ Nur für autorisierte Sicherheitstests!
❌ Illegal, wenn ohne Erlaubnis verwendet!
❌ Kann Bluetooth-Geräte stören oder beschädigen.

Nutze dieses Tool nur auf eigenen Geräten oder mit ausdrücklicher Genehmigung.

📌 GitHub-Repo
🔗 https://github.com/deinusername/ubertooth-evil-toolkit

Füge eine README.md und requirements.txt hinzu, um die Installation zu vereinfachen.

🛡️ Verantwortungsvolle Nutzung
Dieses Projekt dient ausschließlich Forschungszwecken. Der Autor übernimmt keine Haftung für Missbrauch.

Happy (ethical) Hacking! 🚀🔊
