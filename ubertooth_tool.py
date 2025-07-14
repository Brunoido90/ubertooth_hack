#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from datetime import datetime
import usb.core
import usb.util
import signal
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

class UbertoothDetector:
    def __init__(self):
        self.UBERTOOTH_VENDOR_ID = 0x1D50
        self.UBERTOOTH_PRODUCT_ID = 0x6002
        self.DFU_MODE_PRODUCT_ID = 0x6007
        self.device = None

    def detect(self):
        """Check if Ubertooth is connected in normal or DFU mode"""
        self.device = usb.core.find(idVendor=self.UBERTOOTH_VENDOR_ID,
                                  idProduct=self.UBERTOOTH_PRODUCT_ID)
        
        if self.device is None:
            # Check DFU mode
            self.device = usb.core.find(idVendor=self.UBERTOOTH_VENDOR_ID,
                                      idProduct=self.DFU_MODE_PRODUCT_ID)
            if self.device:
                return "dfu"
            return None
        return "normal"

    def reset_device(self):
        """Reset USB device"""
        try:
            self.device.reset()
            return True
        except:
            return False

class UberEvil:
    def __init__(self):
        self.running = True
        self.current_process = None
        self.detector = UbertoothDetector()
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print(f"\n{Fore.RED}💀 TERMINATING ALL ATTACKS!{Style.RESET_ALL}")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        if self.current_process:
            self.current_process.terminate()

    def show_banner(self):
        print(f"""{Fore.MAGENTA}
  ___ _ _ _   ___ ___ _____ ___ ___ 
 | _ | | | |_| _ ) _|_   _|_ _/ _ \\
 | _ |_  _|_  _) _| | |  | | (_) |
 |___| |_| |_| |_|___| |_| |_|\___/
                                    
-------------------------------------
   UBERTOOTH EVIL SUITE v666
  Now with 100% more USB detection!
-------------------------------------
{Style.RESET_ALL}""")

    def check_privileges(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}🚫 ERROR: This weapon requires root!{Style.RESET_ALL}")
            print(f"Run: {Fore.YELLOW}sudo {sys.argv[0]} --destroy{Style.RESET_ALL}")
            sys.exit(1)

    def ensure_ubertooth_ready(self):
        """Check and prepare Ubertooth"""
        status = self.detector.detect()
        
        if status == "dfu":
            print(f"{Fore.YELLOW}⚠️ Ubertooth in DFU mode. Flashing firmware...{Style.RESET_ALL}")
            self.run_attack("ubertooth-dfu -d bluetooth_rxtx.dfu -U")
            time.sleep(2)  # Wait for reboot
            status = self.detector.detect()
        
        if not status:
            print(f"{Fore.RED}🚨 Ubertooth NOT FOUND!{Style.RESET_ALL}")
            print("1. Check USB connection")
            print("2. Try different USB port")
            print("3. Verify with: lsusb | grep Ubertooth")
            return False
        
        print(f"{Fore.GREEN}⚡ Ubertooth READY for mayhem!{Style.RESET_ALL}")
        return True

    def run_attack(self, cmd, timeout=None):
        try:
            print(f"\n{Fore.RED}💥 LAUNCHING: {Fore.YELLOW}{cmd}{Style.RESET_ALL}")
            self.current_process = subprocess.Popen(cmd, shell=True,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE,
                                                  text=True)
            
            if timeout:
                try:
                    stdout, stderr = self.current_process.communicate(timeout=timeout)
                except subprocess.TimeoutExpired:
                    self.current_process.kill()
                    print(f"{Fore.YELLOW}⌛ Attack timed out{Style.RESET_ALL}")
                    return False
            else:
                stdout, stderr = self.current_process.communicate()

            if stdout: print(stdout.strip())
            if stderr: print(f"{Fore.RED}ERROR:{Style.RESET_ALL} {stderr.strip()}")
            
            return self.current_process.returncode == 0
            
        except Exception as e:
            print(f"{Fore.RED}💣 ATTACK FAILED: {str(e)}{Style.RESET_ALL}")
            return False

    def bt_classic_chaos(self):
        """Bluetooth Classic attacks"""
        while True:
            self.show_banner()
            print(f"\n{Style.BRIGHT}=== Bluetooth Classic ==={Style.RESET_ALL}")
            print("1. Sniff ACL packets")
            print("2. Sniff voice (SCO)")
            print("3. Bruteforce LAPs")
            print("4. Channel hopping jam")
            print("5. Back to main menu")
            
            choice = input("\nSelect weapon: ")
            
            if choice == "1":
                self.run_attack("ubertooth-bt -A -f")
            elif choice == "2":
                self.run_attack("ubertooth-bt -S -f")
            elif choice == "3":
                self.run_attack("ubertooth-bt -B -f")  # Bruteforce mode
            elif choice == "4":
                self.run_attack("ubertooth-jam -b -H")
            elif choice == "5":
                break
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")

    def main(self):
        self.check_privileges()
        if not self.ensure_ubertooth_ready():
            sys.exit(1)
        
        while self.running:
            self.show_banner()
            print(f"\n{Style.BRIGHT}=== MAIN MENU ==={Style.RESET_ALL}")
            print(f"{Fore.GREEN}1. Bluetooth Classic Chaos{Style.RESET_ALL}")
            print(f"{Fore.BLUE}2. BLE Mayhem{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}3. WiFi/2.4GHz Terror{Style.RESET_ALL}")
            print(f"{Fore.RED}4. Nuclear Options{Style.RESET_ALL}")
            print(f"{Fore.WHITE}5. Exit{Style.RESET_ALL}")
            
            choice = input("\nSelect weapon: ")
            
            if choice == "1":
                self.bt_classic_chaos()
            elif choice == "5":
                print(f"\n{Fore.RED}💀 Shutting down...{Style.RESET_ALL}")
                self.running = False
            else:
                print(f"{Fore.RED}Feature coming soon!{Style.RESET_ALL}")

if __name__ == "__main__":
    weapon = UberEvil()
    try:
        weapon.main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}🚨 Emergency shutdown!{Style.RESET_ALL}")
        weapon.cleanup()
    except Exception as e:
        print(f"\n{Fore.RED}💥 CATASTROPHIC FAILURE: {str(e)}{Style.RESET_ALL}")
        weapon.cleanup()
