Ubertooth All-in-One Bluetooth Hacking Tool
Dieses Tool nutzt Ubertooth-One zur Analyse, Überwachung und Manipulation von Bluetooth Classic (BR/EDR) und Bluetooth Low Energy (BLE). Es kombiniert mehrere Ubertooth-Funktionen in einem einzigen, einfach zu bedienenden Python-Skript.

🔧 Funktionen
✅ Bluetooth-Scanning (--scan) – Erkennt alle sichtbaren Bluetooth-Geräte
✅ Packet Sniffing (--sniff [Kanal]) – Fängt Bluetooth-Pakete auf einem bestimmten Kanal ab
✅ Jamming (Denial-of-Service) (--jam) – Stört Bluetooth-Kommunikation gezielt
✅ Geräte verfolgen (--follow [MAC]) – Überwacht den Verkehr eines bestimmten Geräts
✅ Datei senden (--send [MAC] [FILE]) – Sendet eine Datei an ein Bluetooth-Gerät
✅ Datei empfangen (--receive [PFAD]) – Wartet auf eine eingehende Datei
✅ Signalstärke-Messung (RSSI) (--rssi [MAC]) – Misst die Signalstärke eines Geräts (Tracking)
✅ Audio-Pakete sniffen (--audio-sniff) – Fängt Bluetooth-Audio-Daten zur Analyse ab

📌 Installation
Installiere Ubertooth-Tools & Abhängigkeiten:
bash
Kopieren
Bearbeiten
sudo apt install ubertooth obexftp obexftpd
Führe das Tool aus:
bash
Kopieren
Bearbeiten
python3 ubertooth_hack.py --scan
⚠ Rechtlicher Hinweis
Dieses Tool ist ausschließlich für Sicherheitsforschung & Penetration-Testing in autorisierten Umgebungen gedacht.
Missbrauch ist illegal! Nutze es nur mit Erlaubnis.
