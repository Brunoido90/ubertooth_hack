#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from datetime import datetime

# Farben fürs Terminal
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def show_banner():
    print(f"""{colors.PURPLE}
  ___ _ _ _   ___ ___ _____ ___ ___ 
 | _ | | | |_| _ ) _|_   _|_ _/ _ \\
 | _ |_  _|_  _) _| | |  | | (_) |
 |___| |_| |_| |_|___| |_| |_|\___/
                                    
-------------------------------------
   Ubertooth Swiss Army Knife v2.0
  All-in-One Bluetooth Toolbox
-------------------------------------
{colors.END}""")

def check_root():
    if os.geteuid() != 0:
        print(f"{colors.RED}ERROR: Run as root!{colors.END}")
        print(f"sudo {sys.argv[0]}")
        sys.exit(1)

def check_ubertooth():
    try:
        result = subprocess.run(["ubertooth-util", "-v"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        if "Firmware version" in result.stdout:
            return True
        print(f"{colors.RED}Ubertooth not found!{colors.END}")
        print(f"Connect Ubertooth and run: {colors.YELLOW}ubertooth-dfu -d bluetooth_rxtx.dfu -U{colors.END}")
        return False
    except FileNotFoundError:
        print(f"{colors.RED}Ubertooth tools not installed!{colors.END}")
        print(f"Install with: {colors.YELLOW}sudo apt install ubertooth{colors.END}")
        return False

def run_cmd(cmd, timeout=60):
    try:
        print(f"\n{colors.CYAN}Running: {colors.YELLOW}{cmd}{colors.END}")
        process = subprocess.Popen(cmd, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Live output handling
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Error handling
        stderr = process.stderr.read()
        if stderr:
            print(f"{colors.RED}Error:{colors.END} {stderr}")
            
        return True
    except Exception as e:
        print(f"{colors.RED}Critical error:{colors.END} {str(e)}")
        return False
    finally:
        process.terminate()

def bt_classic_menu():
    while True:
        show_banner()
        print(f"\n{colors.BOLD}=== Bluetooth Classic ==={colors.END}")
        print("1. Sniff ACL packets")
        print("2. Sniff SCO packets (voice)")
        print("3. Sniff with LAP (e.g. 0x9E8B33)")
        print("4. Channel hopping sniff")
        print("5. Capture to PCAP")
        print("6. Back to main menu")
        
        choice = input("\nSelect: ")
        
        if choice == "1":
            run_cmd("ubertooth-bt -A -f")
        elif choice == "2":
            run_cmd("ubertooth-bt -S -f")
        elif choice == "3":
            lap = input("Enter LAP (e.g. 0x9E8B33): ")
            run_cmd(f"ubertooth-bt -l {lap} -f")
        elif choice == "4":
            run_cmd("ubertooth-bt -H -f")
        elif choice == "5":
            pcap = f"bt_classic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
            run_cmd(f"ubertooth-bt -c {pcap}")
        elif choice == "6":
            break
        else:
            print(f"{colors.RED}Invalid choice!{colors.END}")

def ble_menu():
    while True:
        show_banner()
        print(f"\n{colors.BOLD}=== BLE Menu ==={colors.END}")
        print("1. Sniff advertisements")
        print("2. Sniff data channels")
        print("3. Follow specific device")
        print("4. Active scan")
        print("5. Capture to PCAP")
        print("6. Back to main menu")
        
        choice = input("\nSelect: ")
        
        if choice == "1":
            run_cmd("ubertooth-btle -a -f")
        elif choice == "2":
            run_cmd("ubertooth-btle -f")
        elif choice == "3":
            mac = input("Enter BLE MAC (e.g. 01:23:45:67:89:AB): ")
            run_cmd(f"ubertooth-btle -t {mac} -f")
        elif choice == "4":
            run_cmd("ubertooth-btle -s")
        elif choice == "5":
            pcap = f"ble_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
            run_cmd(f"ubertooth-btle -c {pcap}")
        elif choice == "6":
            break
        else:
            print(f"{colors.RED}Invalid choice!{colors.END}")

def spectrum_menu():
    while True:
        show_banner()
        print(f"\n{colors.BOLD}=== Spectrum Tools ==={colors.END}")
        print("1. Full 2.4GHz scan")
        print("2. Bluetooth channels scan")
        print("3. Custom frequency scan")
        print("4. Continuous monitoring")
        print("5. Back to main menu")
        
        choice = input("\nSelect: ")
        
        if choice == "1":
            run_cmd("ubertooth-specan")
        elif choice == "2":
            run_cmd("ubertooth-specan -b")
        elif choice == "3":
            start = input("Start freq (MHz): ")
            end = input("End freq (MHz): ")
            step = input("Step size (MHz): ")
            run_cmd(f"ubertooth-specan -s {start} -e {end} -l {step}")
        elif choice == "4":
            run_cmd("ubertooth-specan -l 0")
        elif choice == "5":
            break
        else:
            print(f"{colors.RED}Invalid choice!{colors.END}")

def advanced_menu():
    while True:
        show_banner()
        print(f"\n{colors.BOLD}=== Advanced Tools ==={colors.END}")
        print("1. Transmit test packets")
        print("2. Jam specific channel")
        print("3. RSSI monitoring")
        print("4. Device discovery")
        print("5. Firmware update")
        print("6. Ubertooth info")
        print("7. Back to main menu")
        
        choice = input("\nSelect: ")
        
        if choice == "1":
            run_cmd("ubertooth-tx")
        elif choice == "2":
            channel = input("Channel (0-79): ")
            run_cmd(f"ubertooth-jam -c {channel}")
        elif choice == "3":
            run_cmd("ubertooth-rssi")
        elif choice == "4":
            run_cmd("ubertooth-scan")
        elif choice == "5":
            print("\nUpdating firmware...")
            run_cmd("ubertooth-dfu -d bluetooth_rxtx.dfu -U")
        elif choice == "6":
            run_cmd("ubertooth-util -v && ubertooth-util -s")
            input("\nPress Enter to continue...")
        elif choice == "7":
            break
        else:
            print(f"{colors.RED}Invalid choice!{colors.END}")

def main():
    check_root()
    if not check_ubertooth():
        sys.exit(1)
    
    while True:
        show_banner()
        print(f"\n{colors.BOLD}=== Main Menu ==={colors.END}")
        print(f"{colors.GREEN}1. Bluetooth Classic{colors.END}")
        print(f"{colors.BLUE}2. Bluetooth Low Energy (BLE){colors.END}")
        print(f"{colors.YELLOW}3. Spectrum Analysis{colors.END}")
        print(f"{colors.RED}4. Advanced Tools{colors.END}")
        print(f"{colors.WHITE}5. Exit{colors.END}")
        
        choice = input("\nSelect: ")
        
        if choice == "1":
            bt_classic_menu()
        elif choice == "2":
            ble_menu()
        elif choice == "3":
            spectrum_menu()
        elif choice == "4":
            advanced_menu()
        elif choice == "5":
            print("\nExiting...")
            break
        else:
            print(f"{colors.RED}Invalid choice!{colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        print(f"\n{colors.RED}Fatal error:{colors.END} {str(e)}")
