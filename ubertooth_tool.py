#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH LED SCANNER v666 - MIT SICHTBAREM BLINKEN

import os
import sys
import re
import time
import signal
import subprocess
import usb.core
import colorama
from colorama import Fore, Style

colorama.init()

class UberLedScanner:
    def __init__(self):
        self.targets = []
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
            print(f"{Fore.RED}🚨 Ubertooth not found!{Style.RESET_ALL}")
            sys.exit(1)

    def show_banner(self):
        os.system('clear')
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH LED SCANNER v666
   • Sichtbares Blinken während Scan •
   • Kein Zweifel ob es arbeitet    •
 ------------------------------------
{Style.RESET_ALL}""")

    def blink_led(self, duration=15):
        """Blinkt die LED während des Scans"""
        print(f"{Fore.YELLOW}💡 LED blinkt jetzt während des Scans...{Style.RESET_ALL}")
        os.system("ubertooth-util -l")  # LED blinken starten
        time.sleep(duration)
        os.system("ubertooth-util -L")  # LED ausschalten

    def scan_devices(self):
        """Scannt Geräte mit sichtbarem LED-Blinken"""
        self.show_banner()
        
        # Starte LED-Blinken in einem separaten Thread
        led_thread = Thread(target=self.blink_led)
        led_thread.start()
        
        # Haupt-Scan
        print(f"{Fore.CYAN}🔍 Scanning for targets (15 seconds)...{Style.RESET_ALL}")
        result = subprocess.run(["ubertooth-scan", "-t", "15"], 
                              capture_output=True, text=True)
        
        # Parse Ergebnisse
        self.targets = []
        for line in result.stdout.split('\n'):
            if 'BD_ADDR' in line:
                mac = re.search(r'(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})', line)
                if mac:
                    self.targets.append(mac.group(1))
        
        led_thread.join()  # Warte bis LED-Thread fertig ist
        return len(self.targets) > 0

    def show_results(self):
        """Zeigt Scan-Ergebnisse"""
        self.show_banner()
        print(f"\n{Fore.GREEN}=== GEFUNDENE ZIELE ==={Style.RESET_ALL}")
        for i, target in enumerate(self.targets, 1):
            print(f"{i}. {target}")
        print("\n")

    def cleanup(self, sig=None, frame=None):
        print(f"\n{Fore.RED}🛑 Beende alle Prozesse...{Style.RESET_ALL}")
        os.system("ubertooth-util -L")  # LED ausschalten
        os.system("pkill -f 'ubertooth'")
        sys.exit(0)

    def main(self):
        while self.running:
            if self.scan_devices():
                self.show_results()
                input("Drücke Enter für neuen Scan...")
            else:
                print(f"{Fore.RED}Keine Geräte gefunden!{Style.RESET_ALL}")
                time.sleep(2)

if __name__ == "__main__":
    scanner = UberLedScanner()
    try:
        scanner.main()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    finally:
        scanner.cleanup()
