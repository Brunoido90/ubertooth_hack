#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from datetime import datetime
import signal
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

class UberTool:
    def __init__(self):
        self.running = True
        self.current_process = None
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print(f"\n{Fore.RED}Received shutdown signal! Terminating processes...{Style.RESET_ALL}")
        if self.current_process:
            self.current_process.terminate()
        self.running = False
        sys.exit(0)

    def show_banner(self):
        print(f"""{Fore.MAGENTA}
  ___ _ _ _   ___ ___ _____ ___ ___ 
 | _ | | | |_| _ ) _|_   _|_ _/ _ \\
 | _ |_  _|_  _) _| | |  | | (_) |
 |___| |_| |_| |_|___| |_| |_|\___/
                                    
-------------------------------------
   Ubertooth Swiss Army Knife v3.0
  Ultimate Bluetooth/WiFi Toolbox
-------------------------------------
{Style.RESET_ALL}""")

    def check_root(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}ERROR: This tool requires root privileges!{Style.RESET_ALL}")
            print(f"Please run with: sudo {sys.argv[0]}")
            sys.exit(1)

    def check_ubertooth(self):
        try:
            result = subprocess.run(["ubertooth-util", "-v"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=5)
            if "Firmware version" in result.stdout:
                return True
            
            print(f"{Fore.RED}Ubertooth device not responding!{Style.RESET_ALL}")
            print(f"Connect Ubertooth and run: {Fore.YELLOW}ubertooth-dfu -d bluetooth_rxtx.dfu -U{Style.RESET_ALL}")
            return False
            
        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}Ubertooth not responding!{Style.RESET_ALL}")
            return False
        except FileNotFoundError:
            print(f"{Fore.RED}Ubertooth tools not installed!{Style.RESET_ALL}")
            print(f"Install with: {Fore.YELLOW}sudo apt install ubertooth{Style.RESET_ALL}")
            return False

    def run_cmd(self, cmd, timeout=None, background=False):
        try:
            print(f"\n{Fore.CYAN}Executing: {Fore.YELLOW}{cmd}{Style.RESET_ALL}")
            
            if background:
                process = subprocess.Popen(cmd, shell=True,
                                         stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL)
                return process
            
            process = subprocess.Popen(cmd, shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True)
            self.current_process = process
            
            if timeout:
                try:
                    stdout, stderr = process.communicate(timeout=timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"{Fore.YELLOW}Command timed out after {timeout} seconds{Style.RESET_ALL}")
                    return False
            else:
                stdout, stderr = process.communicate()

            if stdout:
                print(stdout.strip())
            if stderr:
                print(f"{Fore.RED}Error:{Style.RESET_ALL} {stderr.strip()}")
            
            return process.returncode == 0
            
        except Exception as e:
            print(f"{Fore.RED}Critical error:{Style.RESET_ALL} {str(e)}")
            return False

    def capture_to_pcap(self, cmd, pcap_name):
        print(f"{Fore.RED}🚀 Starting PCAP capture: {pcap_name}{Style.RESET_ALL}")
        try:
            with open(pcap_name, 'wb') as pcap_file:
                process = subprocess.Popen(cmd, shell=True, 
                                         stdout=pcap_file, 
                                         stderr=subprocess.PIPE)
                self.current_process = process
                
                try:
                    _, stderr = process.communicate(timeout=30)
                    if stderr:
                        print(f"{Fore.RED}Error:{Style.RESET_ALL} {stderr.decode().strip()}")
                except subprocess.TimeoutExpired:
                    print(f"{Fore.YELLOW}Capture still running... Press Ctrl+C to stop{Style.RESET_ALL}")
                    return process
                    
            print(f"{Fore.GREEN}✅ PCAP saved: {pcap_name}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}💥 PCAP error: {e}{Style.RESET_ALL}")
            return False

    def bruteforce_lap(self):
        print(f"{Fore.RED}🔥 Bruteforcing Bluetooth LAPs...{Style.RESET_ALL}")
        common_laps = ["0x9E8B33", "0x8E89BD", "0x0014A9", "0x000000", "0xFFFFFFFF"]
        
        for lap in common_laps:
            print(f"{Fore.YELLOW}⚡ Trying LAP: {lap}{Style.RESET_ALL}")
            if self.run_cmd(f"ubertooth-bt -l {lap} -f -t 10"):
                print(f"{Fore.GREEN}🎯 HIT: Device found with LAP: {lap}{Style.RESET_ALL}")
                return lap
                
        print(f"{Fore.RED}No devices found with common LAPs{Style.RESET_ALL}")
        return None

    def ble_spoof(self, mac=None, name="EVIL_DEVICE"):
        if not mac:
            mac = "00:11:22:33:44:55"
            
        print(f"{Fore.RED}👻 Creating fake BLE device: {name} ({mac}){Style.RESET_ALL}")
        return self.run_cmd(f"ubertooth-btle -a -A -M -i {mac} -n '{name}'", background=True)

    def wifi_bt_jam(self, channel=6):
        print(f"{Fore.RED}📡 WiFi/BT Channel {channel} JAMMING!{Style.RESET_ALL}")
        return self.run_cmd(f"ubertooth-jam -c {channel} -W", background=True)

    def firmware_recovery(self):
        print(f"{Fore.RED}💀 Attempting firmware recovery...{Style.RESET_ALL}")
        self.run_cmd("ubertooth-dfu --unbrick -U")
        time.sleep(2)
        return self.check_ubertooth()

    def bt_classic_menu(self):
        while self.running:
            self.show_banner()
            print(f"\n{Style.BRIGHT}=== Bluetooth Classic ==={Style.RESET_ALL}")
            print("1. Sniff ACL packets")
            print("2. Sniff SCO packets (voice)")
            print("3. Sniff with specific LAP")
            print("4. Bruteforce common LAPs")
            print("5. Channel hopping sniff")
            print("6. Capture to PCAP")
            print("7. Back to main menu")
            
            choice = input("\nSelect: ")
            
            if choice == "1":
                self.run_cmd("ubertooth-bt -A -f")
            elif choice == "2":
                self.run_cmd("ubertooth-bt -S -f")
            elif choice == "3":
                lap = input("Enter LAP (e.g. 0x9E8B33): ")
                self.run_cmd(f"ubertooth-bt -l {lap} -f")
            elif choice == "4":
                self.bruteforce_lap()
            elif choice == "5":
                self.run_cmd("ubertooth-bt -H -f")
            elif choice == "6":
                pcap = f"bt_classic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
                self.capture_to_pcap(f"ubertooth-bt -c {pcap}", pcap)
            elif choice == "7":
                break
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            input("\nPress Enter to continue...")

    def ble_menu(self):
        while self.running:
            self.show_banner()
            print(f"\n{Style.BRIGHT}=== BLE Menu ==={Style.RESET_ALL}")
            print("1. Sniff advertisements")
            print("2. Sniff data channels")
            print("3. Follow specific device")
            print("4. Active scan")
            print("5. Spoof BLE device")
            print("6. Capture to PCAP")
            print("7. Back to main menu")
            
            choice = input("\nSelect: ")
            
            if choice == "1":
                self.run_cmd("ubertooth-btle -a -f")
            elif choice == "2":
                self.run_cmd("ubertooth-btle -f")
            elif choice == "3":
                mac = input("Enter BLE MAC (e.g. 01:23:45:67:89:AB): ")
                self.run_cmd(f"ubertooth-btle -t {mac} -f")
            elif choice == "4":
                self.run_cmd("ubertooth-btle -s")
            elif choice == "5":
                mac = input(f"Enter MAC to spoof [{Fore.YELLOW}leave blank for random{Style.RESET_ALL}]: ")
                name = input("Enter device name: ")
                self.ble_spoof(mac if mac else None, name or "EVIL_DEVICE")
            elif choice == "6":
                pcap = f"ble_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
                self.capture_to_pcap(f"ubertooth-btle -c {pcap}", pcap)
            elif choice == "7":
                break
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            input("\nPress Enter to continue...")

    def spectrum_menu(self):
        while self.running:
            self.show_banner()
            print(f"\n{Style.BRIGHT}=== Spectrum Tools ==={Style.RESET_ALL}")
            print("1. Full 2.4GHz scan")
            print("2. Bluetooth channels scan")
            print("3. Custom frequency scan")
            print("4. Continuous monitoring")
            print("5. WiFi/BT channel jammer")
            print("6. Back to main menu")
            
            choice = input("\nSelect: ")
            
            if choice == "1":
                self.run_cmd("ubertooth-specan")
            elif choice == "2":
                self.run_cmd("ubertooth-specan -b")
            elif choice == "3":
                start = input("Start freq (MHz): ")
                end = input("End freq (MHz): ")
                step = input("Step size (MHz): ")
                self.run_cmd(f"ubertooth-specan -s {start} -e {end} -l {step}")
            elif choice == "4":
                self.run_cmd("ubertooth-specan -l 0")
            elif choice == "5":
                channel = input("Channel to jam (0-79, default 6): ")
                self.wifi_bt_jam(int(channel) if channel.isdigit() else 6)
            elif choice == "6":
                break
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            input("\nPress Enter to continue...")

    def advanced_menu(self):
        while self.running:
            self.show_banner()
            print(f"\n{Style.BRIGHT}=== Advanced Tools ==={Style.RESET_ALL}")
            print("1. Transmit test packets")
            print("2. Jam specific channel")
            print("3. RSSI monitoring")
            print("4. Device discovery")
            print("5. Firmware update")
            print("6. Firmware recovery (unbrick)")
            print("7. Ubertooth info")
            print("8. Back to main menu")
            
            choice = input("\nSelect: ")
            
            if choice == "1":
                self.run_cmd("ubertooth-tx")
            elif choice == "2":
                channel = input("Channel (0-79): ")
                self.run_cmd(f"ubertooth-jam -c {channel}")
            elif choice == "3":
                self.run_cmd("ubertooth-rssi")
            elif choice == "4":
                self.run_cmd("ubertooth-scan")
            elif choice == "5":
                print("\nUpdating firmware...")
                self.run_cmd("ubertooth-dfu -d bluetooth_rxtx.dfu -U")
            elif choice == "6":
                self.firmware_recovery()
            elif choice == "7":
                self.run_cmd("ubertooth-util -v && ubertooth-util -s")
            elif choice == "8":
                break
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            input("\nPress Enter to continue...")

    def main(self):
        self.check_root()
        if not self.check_ubertooth():
            sys.exit(1)
        
        while self.running:
            self.show_banner()
            print(f"\n{Style.BRIGHT}=== Main Menu ==={Style.RESET_ALL}")
            print(f"{Fore.GREEN}1. Bluetooth Classic{Style.RESET_ALL}")
            print(f"{Fore.BLUE}2. Bluetooth Low Energy (BLE){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}3. Spectrum Analysis{Style.RESET_ALL}")
            print(f"{Fore.RED}4. Advanced Tools{Style.RESET_ALL}")
            print(f"{Fore.WHITE}5. Exit{Style.RESET_ALL}")
            
            choice = input("\nSelect: ")
            
            if choice == "1":
                self.bt_classic_menu()
            elif choice == "2":
                self.ble_menu()
            elif choice == "3":
                self.spectrum_menu()
            elif choice == "4":
                self.advanced_menu()
            elif choice == "5":
                print("\nExiting...")
                self.running = False
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    tool = UberTool()
    try:
        tool.main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n{Fore.RED}Fatal error:{Style.RESET_ALL} {str(e)}")
    finally:
        if tool.current_process:
            tool.current_process.terminate()
