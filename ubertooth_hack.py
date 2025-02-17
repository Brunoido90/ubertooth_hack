import os
import subprocess
import argparse
import logging
from time import sleep

# Logging einrichten
def setup_logging():
    logging.basicConfig(filename="bluetooth_tool.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

# Hilfsfunktion zum Ausführen von Shell-Befehlen
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Fehler beim Ausführen des Befehls: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        logging.error(f"Ausnahme aufgetreten: {e}")
        return None

# Bluetooth-Geräte scannen und Liste zurückgeben
def scan_devices():
    logging.info("Starte Bluetooth-Scan...")
    print("[+] Scanne nach Bluetooth-Geräten...")
    output = run_command("ubertooth-scan")
    if output:
        devices = []
        for line in output.splitlines():
            if "MAC:" in line:
                mac = line.split("MAC:")[1].strip().split()[0]
                name = line.split("Name:")[1].strip() if "Name:" in line else "Unbekannt"
                devices.append((mac, name))
        return devices
    else:
        print("[!] Scan fehlgeschlagen.")
        return []

# Gerät auswählen
def select_device(devices):
    if not devices:
        print("[!] Keine Geräte gefunden.")
        return None

    print("\nGefundene Geräte:")
    for i, (mac, name) in enumerate(devices):
        print(f"{i + 1}) MAC: {mac}, Name: {name}")

    try:
        choice = int(input("Wähle ein Gerät (Nummer): ")) - 1
        if 0 <= choice < len(devices):
            return devices[choice][0]  # Rückgabe der MAC-Adresse
        else:
            print("[!] Ungültige Auswahl.")
            return None
    except ValueError:
        print("[!] Ungültige Eingabe.")
        return None

# Sniffing auf einem bestimmten Kanal
def bluetooth_sniff(channel=39):
    logging.info(f"Starte Sniffing auf Kanal {channel}...")
    print(f"[+] Sniffe auf Kanal {channel}...")
    output = run_command(f"ubertooth-rx -c {channel}")
    if output:
        print(output)
    else:
        print("[!] Sniffing fehlgeschlagen.")

# Bluetooth-Jamming
def bluetooth_jam():
    logging.info("Starte Bluetooth-Jamming...")
    print("[+] Starte Bluetooth-Jamming...")
    output = run_command("ubertooth-jam")
    if output:
        print(output)
    else:
        print("[!] Jamming fehlgeschlagen.")

# Gerät verfolgen
def bluetooth_follow(target_addr):
    logging.info(f"Folge Gerät: {target_addr}...")
    print(f"[+] Folge Gerät: {target_addr}")
    output = run_command(f"ubertooth-follow -t {target_addr}")
    if output:
        print(output)
    else:
        print("[!] Verfolgen fehlgeschlagen.")

# Datei senden
def bluetooth_send_file(target_addr, file_path):
    logging.info(f"Sende Datei {file_path} an {target_addr}...")
    print(f"[+] Sende Datei {file_path} an {target_addr}...")
    output = run_command(f"obexftp --nopath --noconn --uuid none --bluetooth {target_addr} --put {file_path}")
    if output:
        print(output)
    else:
        print("[!] Datei senden fehlgeschlagen.")

# Datei empfangen
def bluetooth_receive_file(save_path):
    logging.info(f"Warte auf eingehende Datei in {save_path}...")
    print("[+] Warte auf eingehende Datei...")
    output = run_command(f"obexftpd -c {save_path}")
    if output:
        print(output)
    else:
        print("[!] Datei empfangen fehlgeschlagen.")

# Signalstärke messen (RSSI)
def bluetooth_rssi(target_addr):
    logging.info(f"Messe Signalstärke von {target_addr}...")
    print(f"[+] Messe Signalstärke von {target_addr}...")
    output = run_command(f"ubertooth-rssi -t {target_addr}")
    if output:
        print(output)
    else:
        print("[!] RSSI-Messung fehlgeschlagen.")

# Audio-Pakete sniffen
def bluetooth_sniff_audio():
    logging.info("Starte Sniffing von Audio-Paketen...")
    print("[+] Starte Sniffing von Audio-Paketen...")
    output = run_command("ubertooth-btbr -f")
    if output:
        print(output)
    else:
        print("[!] Audio-Sniffing fehlgeschlagen.")

# Menü für ausgewähltes Gerät
def device_menu(target_addr):
    while True:
        print(f"\nGerät ausgewählt: {target_addr}")
        print("1) Sniffing starten")
        print("2) Jamming starten")
        print("3) Gerät verfolgen")
        print("4) Datei senden")
        print("5) Datei empfangen")
        print("6) Signalstärke messen")
        print("7) Audio-Pakete sniffen")
        print("8) Zurück zum Hauptmenü")
        choice = input("Wähle eine Option: ")

        if choice == "1":
            channel = input("Gib den Kanal ein (Standard: 39): ")
            bluetooth_sniff(int(channel) if channel else 39)
        elif choice == "2":
            bluetooth_jam()
        elif choice == "3":
            bluetooth_follow(target_addr)
        elif choice == "4":
            file_path = input("Gib den Pfad zur Datei ein: ")
            bluetooth_send_file(target_addr, file_path)
        elif choice == "5":
            save_path = input("Gib das Speicherverzeichnis ein: ")
            bluetooth_receive_file(save_path)
        elif choice == "6":
            bluetooth_rssi(target_addr)
        elif choice == "7":
            bluetooth_sniff_audio()
        elif choice == "8":
            break
        else:
            print("Ungültige Eingabe, bitte erneut versuchen.")

# Hauptmenü
def show_menu():
    setup_logging()
    print("WARNUNG: Dieses Tool darf nur in Umgebungen verwendet werden, in denen du die ausdrückliche Erlaubnis hast.")
    print("Missbrauch kann rechtliche Konsequenzen haben.")
    sleep(2)  # Kurze Pause, damit der Benutzer die Warnung lesen kann

    while True:
        print("\nUbertooth All-in-One Bluetooth Hacking Tool")
        print("1) Bluetooth-Geräte scannen")
        print("2) Beenden")
        choice = input("Wähle eine Option: ")

        if choice == "1":
            devices = scan_devices()
            target_addr = select_device(devices)
            if target_addr:
                device_menu(target_addr)
        elif choice == "2":
            print("Beende das Programm...")
            break
        else:
            print("Ungültige Eingabe, bitte erneut versuchen.")

# Hauptfunktion
def main():
    parser = argparse.ArgumentParser(description="Ubertooth All-in-One Bluetooth Hacking Tool")
    parser.add_argument("-m", "--menu", action="store_true", help="Interaktives Menü starten")
    args = parser.parse_args()

    if args.menu:
        show_menu()
    else:
        print("[!] Kein Befehl angegeben. Nutze --menu für das interaktive Menü.")

if __name__ == "__main__":
    main()
