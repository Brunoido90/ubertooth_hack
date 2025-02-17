import os
import subprocess
import argparse

def run_command(command):
    """Hilfsfunktion zum Ausführen von Shell-Befehlen."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def bluetooth_scan():
    """Scannt nach sichtbaren Bluetooth-Geräten."""
    print("[+] Scanne nach Bluetooth-Geräten...")
    output = run_command("ubertooth-scan")
    print(output)

def bluetooth_sniff(channel=39):
    """Snifft Bluetooth-Pakete auf einem bestimmten Kanal."""
    print(f"[+] Sniffe auf Kanal {channel}...")
    output = run_command(f"ubertooth-rx -c {channel}")
    print(output)

def bluetooth_jam():
    """Stört Bluetooth-Kommunikation durch gezieltes Senden von Paketen."""
    print("[+] Starte Bluetooth-Jamming...")
    output = run_command("ubertooth-jam")
    print(output)

def bluetooth_follow(target_addr):
    """Folgt einem bestimmten Bluetooth-Gerät."""
    print(f"[+] Folge Gerät: {target_addr}")
    output = run_command(f"ubertooth-follow -t {target_addr}")
    print(output)

def bluetooth_send_file(target_addr, file_path):
    """Versucht, eine Datei an ein Bluetooth-Gerät zu senden."""
    print(f"[+] Sende Datei {file_path} an {target_addr}...")
    output = run_command(f"obexftp --nopath --noconn --uuid none --bluetooth {target_addr} --put {file_path}")
    print(output)

def bluetooth_receive_file(save_path):
    """Versucht, eine Datei von einem Bluetooth-Gerät zu empfangen."""
    print("[+] Warte auf eingehende Datei...")
    output = run_command(f"obexftpd -c {save_path}")
    print(output)

def bluetooth_rssi(target_addr):
    """Misst die Signalstärke eines Bluetooth-Geräts (Tracking)."""
    print(f"[+] Messe Signalstärke von {target_addr}...")
    output = run_command(f"ubertooth-rssi -t {target_addr}")
    print(output)

def bluetooth_sniff_audio():
    """Snifft Bluetooth-Audio-Pakete (erfordert manuelle Analyse)."""
    print("[+] Starte Sniffing von Audio-Paketen...")
    output = run_command("ubertooth-btbr -f")
    print(output)

def show_menu():
    """Zeigt ein interaktives Menü für die Benutzersteuerung."""
    while True:
        print("\nUbertooth All-in-One Bluetooth Hacking Tool")
        print("1) Bluetooth-Scan")
        print("2) Sniffing starten")
        print("3) Jamming starten")
        print("4) Gerät verfolgen")
        print("5) Datei senden")
        print("6) Datei empfangen")
        print("7) Signalstärke messen")
        print("8) Audio-Pakete sniffen")
        print("9) Beenden")
        choice = input("Wähle eine Option: ")

        if choice == "1":
            bluetooth_scan()
        elif choice == "2":
            channel = input("Gib den Kanal ein (Standard: 39): ")
            bluetooth_sniff(int(channel) if channel else 39)
        elif choice == "3":
            bluetooth_jam()
        elif choice == "4":
            target = input("Gib die MAC-Adresse des Geräts ein: ")
            bluetooth_follow(target)
        elif choice == "5":
            target = input("Gib die MAC-Adresse des Zielgeräts ein: ")
            file_path = input("Gib den Pfad zur Datei ein: ")
            bluetooth_send_file(target, file_path)
        elif choice == "6":
            save_path = input("Gib das Speicherverzeichnis ein: ")
            bluetooth_receive_file(save_path)
        elif choice == "7":
            target = input("Gib die MAC-Adresse des Geräts ein: ")
            bluetooth_rssi(target)
        elif choice == "8":
            bluetooth_sniff_audio()
        elif choice == "9":
            print("Beende das Programm...")
            break
        else:
            print("Ungültige Eingabe, bitte erneut versuchen.")

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
