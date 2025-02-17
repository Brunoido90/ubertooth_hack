Ubertooth All-in-One Bluetooth Hacking Tool
Dieses Python-Skript ist ein All-in-One-Tool für die Interaktion mit Bluetooth-Geräten unter Verwendung der Ubertooth-Hardware. Es bietet eine benutzerfreundliche, menübasierte Schnittstelle, um verschiedene Bluetooth-Hacking-Aktionen durchzuführen, wie z. B. Scannen, Sniffing, Jamming, Dateiübertragung und mehr. Das Tool ist darauf ausgelegt, die Arbeit mit Bluetooth-Geräten zu vereinfachen, indem es automatisch Geräte scannt und es dem Benutzer ermöglicht, ein Gerät aus einer Liste auszuwählen, ohne die MAC-Adresse manuell eingeben zu müssen.

Funktionen
Bluetooth-Geräte scannen:

Scannt nach sichtbaren Bluetooth-Geräten in der Umgebung.

Zeigt eine Liste der gefundenen Geräte mit MAC-Adresse und Namen an.

Geräteauswahl:

Der Benutzer kann ein Gerät aus der Liste auswählen, ohne die MAC-Adresse manuell eingeben zu müssen.

Sniffing:

Snifft Bluetooth-Pakete auf einem bestimmten Kanal (Standard: Kanal 39).

Jamming:

Stört die Bluetooth-Kommunikation durch gezieltes Senden von Paketen.

Gerät verfolgen:

Verfolgt ein bestimmtes Bluetooth-Gerät und zeigt dessen Aktivität an.

Datei senden:

Versucht, eine Datei an ein ausgewähltes Bluetooth-Gerät zu senden.

Datei empfangen:

Versucht, eine Datei von einem Bluetooth-Gerät zu empfangen.

Signalstärke messen (RSSI):

Misst die Signalstärke eines Bluetooth-Geräts, um es zu verfolgen.

Audio-Pakete sniffen:

Snifft Bluetooth-Audio-Pakete (erfordert manuelle Analyse).

Benutzerfreundliches Menü:

Ein interaktives Menü führt den Benutzer durch die verfügbaren Optionen.

Wie man das Tool verwendet
Voraussetzungen:

Ubertooth-Hardware und die entsprechenden Tools (ubertooth, hcitool, obexftp, obexftpd).

Python 3 muss installiert sein.

Skript ausführen:

bash
Copy
python3 ubertooth_tool.py --menu
Menüoptionen:

Bluetooth-Geräte scannen: Scannt nach Geräten und zeigt eine Liste an.

Gerät auswählen: Wähle ein Gerät aus der Liste aus.

Aktionen ausführen: Nach der Auswahl eines Geräts kannst du Sniffing, Jamming, Datei senden/empfangen usw. durchführen.

Beispielablauf
Skript starten:

bash
Copy
python3 ubertooth_tool.py --menu
Bluetooth-Geräte scannen:

Wähle Option 1, um nach Geräten zu scannen.

Das Skript zeigt eine Liste der gefundenen Geräte an.

Gerät auswählen:

Wähle ein Gerät aus der Liste (z. B. 1 für das erste Gerät).

Aktion auswählen:

Wähle eine Aktion aus dem Untermenü (z. B. 1 für Sniffing).

Wichtige Hinweise
Ethik und Rechtliches:

Dieses Tool darf nur in autorisierten Umgebungen verwendet werden. Der Missbrauch von Bluetooth-Hacking-Tools kann rechtliche Konsequenzen haben. Stelle sicher, dass du die Erlaubnis hast, die Geräte zu scannen oder zu manipulieren, bevor du dieses Tool verwendest.
