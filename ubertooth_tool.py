#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH ONE ALL-IN-ONE TOOLKIT

import os
import sys
import time
import signal
import subprocess
import colorama
from colorama import Fore, Style

colorama.init()

class UberToolkit:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGINT, self.exit_tool)
        self.check_root()
        self.main_menu()

    def check_root(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}Run as root: sudo {sys.argv[0]}{Style.RESET_ALL}")
            sys.exit(1)

    def exit_tool(self, sig=None, frame=None):
        print(f"\n{Fore.YELLOW}Stopping all operations...{Style.RESET_ALL}")
        os.system("pkill -f 'ubertooth'")
        self.running = False
        sys.exit(0)

    def show_banner(self):
        os.system('clear')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH ONE ALL-IN-ONE TOOLKIT
 ------------------------------------
{Style.RESET_ALL}""")

    def run_cmd(self, cmd):
        print(f"\n{Fore.CYAN}Executing: {cmd}{Style.RESET_ALL}")
        os.system(cmd)
        input("\nPress Enter to continue...")

    def main_menu(self):
        while self.running:
            self.show_banner()
            print(f"{Fore.GREEN}=== BLUETOOTH CLASSIC ==={Style.RESET_ALL}")
            print("1. Scan for devices (ubertooth-scan)")
            print("2. Sniff ACL data (ubertooth-bt -A)")
            print("3. Sniff voice calls (ubertooth-bt -S)")
            print("4. Jam specific device (ubertooth-jam -t MAC)")
            
            print(f"\n{Fore.BLUE}=== BLUETOOTH LOW ENERGY ==={Style.RESET_ALL}")
            print("5. Sniff BLE ads (ubertooth-btle -a)")
            print("6. Follow BLE device (ubertooth-btle -t MAC)")
            print("7. Spam fake BLE devices (ubertooth-btle -M)")
            
            print(f"\n{Fore.YELLOW}=== TOOLS & UTILITIES ==={Style.RESET_ALL}")
            print("8. Spectrum analyzer (ubertooth-specan)")
            print("9. RSSI monitoring (ubertooth-rssi)")
            print("10. Firmware update (ubertooth-dfu)")
            
            print(f"\n{Fore.RED}=== EXTREME FUNCTIONS ==={Style.RESET_ALL}")
            print("11. Continuous channel hopping jam")
            print("12. Bruteforce LAP detection")
            
            print(f"\n{Fore.WHITE}0. Exit{Style.RESET_ALL}")
            
            choice = input("\nSelect function (0-12): ")
            
            if choice == "1":
                self.run_cmd("ubertooth-scan -t 15")
            elif choice == "2":
                self.run_cmd("ubertooth-bt -A -f")
            elif choice == "3":
                mac = input("Target MAC (or leave blank): ")
                cmd = f"ubertooth-bt -S -f -t {mac}" if mac else "ubertooth-bt -S -f"
                self.run_cmd(cmd)
            elif choice == "4":
                mac = input("Target MAC: ")
                self.run_cmd(f"ubertooth-jam -b -t {mac}")
            elif choice == "5":
                self.run_cmd("ubertooth-btle -a -f")
            elif choice == "6":
                mac = input("Target MAC: ")
                self.run_cmd(f"ubertooth-btle -t {mac} -f")
            elif choice == "7":
                count = input("Number of fake devices: ")
                self.run_cmd(f"ubertooth-btle -a -M -c {count}")
            elif choice == "8":
                self.run_cmd("ubertooth-specan")
            elif choice == "9":
                self.run_cmd("ubertooth-rssi")
            elif choice == "10":
                self.run_cmd("ubertooth-dfu -d bluetooth_rxtx.dfu -U")
            elif choice == "11":
                self.run_cmd("ubertooth-jam -b -H")
            elif choice == "12":
                self.run_cmd("ubertooth-bt -B -f")
            elif choice == "0":
                self.exit_tool()
            else:
                print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        UberToolkit()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
