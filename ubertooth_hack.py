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

def main():
    parser = argparse.ArgumentParser(description="Ubertooth All-in-One Bluetooth Hacking Tool")
    parser.add_argument("-s", "--scan", action="store_true", help="Bluetooth-Scan starten")
    parser.add_argument("-n", "--sniff", type=int, help="Bluetooth-Sniffing auf bestimmtem Kanal")
    parser.add_argument("-j", "--jam", action="store_true", help="Bluetooth-Jamming starten")
    parser.add_argument("-f", "--follow", type=str, help="Einem bestimmten Gerät folgen")
    parser.add_argument("--send", nargs=2, metavar=('TARGET', 'FILE'), help="Datei an ein Gerät senden")
    parser.add_argument("--receive", type=str, help="Eingehende Datei empfangen und speichern")
    parser.add_argument("--rssi", type=str, help="Signalstärke eines Geräts messen")
    parser.add_argument("--audio-sniff", action="store_true", help="Audio-Pakete sniffen")
    
    args = parser.parse_args()
    
    if args.scan:
        bluetooth_scan()
    elif args.sniff:
        bluetooth_sniff(args.sniff)
    elif args.jam:
        bluetooth_jam()
    elif args.follow:
        bluetooth_follow(args.follow)
    elif args.send:
        bluetooth_send_file(args.send[0], args.send[1])
    elif args.receive:
        bluetooth_receive_file(args.receive)
    elif args.rssi:
        bluetooth_rssi(args.rssi)
    elif args.audio_sniff:
        bluetooth_sniff_audio()
    else:
        print("[!] Kein Befehl angegeben. Nutze --help für Optionen.")

if __name__ == "__main__":
    main()
