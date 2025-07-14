#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from datetime import datetime

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    print(r"""
  ___ _ _ _   ___ ___ _____ ___ ___ 
 | _ | | | |_| _ ) _|_   _|_ _/ _ \
 | _ |_  _|_  _) _| | |  | | (_) |
 |___| |_| |_| |_|___| |_| |_|\___/
                                    
=====================================
    Ubertooth Swiss Army Knife
=====================================
""")

def run_command(cmd, capture_output=False):
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, check=True, 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True)
            return result.stdout
        else:
            subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}" if capture_output else f"Error executing command: {e}")
        return None
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return None
    return ""

def save_to_file(data, filename_prefix):
    if not os.path.exists('captures'):
        os.makedirs('captures')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"captures/{filename_prefix}_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(data)
    print(f"Data saved to {filename}")

class UbertoothTool:
    def __init__(self):
        self.running = True
        self.device_info = None
    
    def show_menu(self):
        clear_screen()
        show_banner()
        print("Main Menu:")
        print("1. Bluetooth Classic Operations")
        print("2. Bluetooth Low Energy (BLE) Operations")
        print("3. Spectrum Analysis Tools")
        print("4. Transmission Tools")
        print("5. Device Discovery & Monitoring")
        print("6. Ubertooth Utilities")
        print("7. Advanced Features")
        print("0. Exit")
        print("=====================================")
    
    def bluetooth_classic_menu(self):
        while True:
            clear_screen()
            show_banner()
            print("Bluetooth Classic Operations:")
            print("1. Sniff Bluetooth ACL packets")
            print("2. Sniff Bluetooth SCO packets (voice)")
            print("3. Sniff with specific LAP (Lower Address Part)")
            print("4. Channel hopping sniffing")
            print("5. Capture to PCAP file")
            print("6. Real-time decoding")
            print("7. Back to Main Menu")
            
            choice = input("Select: ")
            
            if choice == "1":
                self.sniff_bluetooth("ACL")
            elif choice == "2":
                self.sniff_bluetooth("SCO")
            elif choice == "3":
                lap = input("Enter LAP (hex, e.g. 0x9E8B33): ")
                self.sniff_bluetooth("LAP", lap)
            elif choice == "4":
                self.sniff_bluetooth("HOP")
            elif choice == "5":
                self.capture_pcap("BTCLASSIC")
            elif choice == "6":
                self.realtime_decode("CLASSIC")
            elif choice == "7":
                break
            else:
                print("Invalid choice")
                time.sleep(1)
    
    def ble_menu(self):
        while True:
            clear_screen()
            show_banner()
            print("Bluetooth Low Energy Operations:")
            print("1. Sniff BLE advertisements")
            print("2. Sniff BLE data channels")
            print("3. Follow specific BLE device")
            print("4. Active scan for BLE devices")
            print("5. Capture to PCAP file")
            print("6. Real-time decoding")
            print("7. Back to Main Menu")
            
            choice = input("Select: ")
            
            if choice == "1":
                self.sniff_ble("ADV")
            elif choice == "2":
                self.sniff_ble("DATA")
            elif choice == "3":
                mac = input("Enter BLE MAC (e.g. 01:23:45:67:89:AB): ")
                self.sniff_ble("FOLLOW", mac)
            elif choice == "4":
                self.scan_ble()
            elif choice == "5":
                self.capture_pcap("BLE")
            elif choice == "6":
                self.realtime_decode("BLE")
            elif choice == "7":
                break
            else:
                print("Invalid choice")
                time.sleep(1)
    
    def spectrum_menu(self):
        while True:
            clear_screen()
            show_banner()
            print("Spectrum Analysis Tools:")
            print("1. Full 2.4GHz spectrum scan")
            print("2. Bluetooth channels scan")
            print("3. Custom frequency range scan")
            print("4. Continuous spectrum monitoring")
            print("5. Measure channel utilization")
            print("6. Back to Main Menu")
            
            choice = input("Select: ")
            
            if choice == "1":
                self.spectrum_scan("FULL")
            elif choice == "2":
                self.spectrum_scan("BT")
            elif choice == "3":
                start = input("Start frequency (MHz): ")
                end = input("End frequency (MHz): ")
                step = input("Step size (MHz): ")
                self.spectrum_scan("CUSTOM", start, end, step)
            elif choice == "4":
                self.spectrum_monitor()
            elif choice == "5":
                self.channel_utilization()
            elif choice == "6":
                break
            else:
                print("Invalid choice")
                time.sleep(1)
    
    def transmission_menu(self):
        while True:
            clear_screen()
            show_banner()
            print("Transmission Tools:")
            print("1. Transmit test packets")
            print("2. Transmit custom packets")
            print("3. Jam specific channel")
            print("4. Jam specific device")
            print("5. Back to Main Menu")
            
            choice = input("Select: ")
            
            if choice == "1":
                self.transmit_packets("TEST")
            elif choice == "2":
                count = input("Packet count: ")
                delay = input("Delay between packets (ms): ")
                self.transmit_packets("CUSTOM", count, delay)
            elif choice == "3":
                channel = input("Bluetooth channel (0-79): ")
                self.jam("CHANNEL", channel)
            elif choice == "4":
                mac = input("Enter target MAC: ")
                self.jam("DEVICE", mac)
            elif choice == "5":
                break
            else:
                print("Invalid choice")
                time.sleep(1)
    
    def discovery_menu(self):
        while True:
            clear_screen()
            show_banner()
            print("Device Discovery & Monitoring:")
            print("1. Discover Bluetooth devices")
            print("2. Discover BLE devices")
            print("3. Monitor RSSI of devices")
            print("4. Continuous device monitoring")
            print("5. Back to Main Menu")
            
            choice = input("Select: ")
            
            if choice == "1":
                self.discover_devices("CLASSIC")
            elif choice == "2":
                self.discover_devices("BLE")
            elif choice == "3":
                self.monitor_rssi()
            elif choice == "4":
                self.continuous_monitoring()
            elif choice == "5":
                break
            else:
                print("Invalid choice")
                time.sleep(1)
    
    def utilities_menu(self):
        while True:
            clear_screen()
            show_banner()
            print("Ubertooth Utilities:")
            print("1. Show Ubertooth info")
            print("2. Update firmware")
            print("3. Reset Ubertooth")
            print("4. Check USB connection")
            print("5. Back to Main Menu")
            
            choice = input("Select: ")
            
            if choice == "1":
                self.show_ubertooth_info()
            elif choice == "2":
                self.update_firmware()
            elif choice == "3":
                self.reset_ubertooth()
            elif choice == "4":
                self.check_usb()
            elif choice == "5":
                break
            else:
                print("Invalid choice")
                time.sleep(1)
    
    def advanced_menu(self):
        while True:
            clear_screen()
            show_banner()
            print("Advanced Features:")
            print("1. Bluetooth PIN cracking")
            print("2. BLE pairing capture")
            print("3. Custom FPGA load")
            print("4. Back to Main Menu")
            
            choice = input("Select: ")
            
            if choice == "1":
                self.pin_cracking()
            elif choice == "2":
                self.capture_pairing()
            elif choice == "3":
                self.load_custom_fpga()
            elif choice == "4":
                break
            else:
                print("Invalid choice")
                time.sleep(1)
    
    # Implementation of all the functions
    def sniff_bluetooth(self, mode, param=None):
        cmd = "ubertooth-bt"
        if mode == "ACL":
            cmd += " -A"
        elif mode == "SCO":
            cmd += " -S"
        elif mode == "LAP":
            cmd += f" -l {param}"
        elif mode == "HOP":
            cmd += " -H"
        
        print(f"\nStarting Bluetooth sniffing in {mode} mode...")
        print("Press Ctrl+C to stop\n")
        run_command(cmd)
    
    def sniff_ble(self, mode, param=None):
        cmd = "ubertooth-btle"
        if mode == "ADV":
            cmd += " -a"
        elif mode == "DATA":
            cmd += " -f"
        elif mode == "FOLLOW":
            cmd += f" -t {param}"
        
        print(f"\nStarting BLE sniffing in {mode} mode...")
        print("Press Ctrl+C to stop\n")
        run_command(cmd)
    
    def scan_ble(self):
        print("\nScanning for BLE devices...")
        output = run_command("ubertooth-btle -s", capture_output=True)
        if output:
            print(output)
            save_to_file(output, "ble_scan")
    
    def spectrum_scan(self, mode, *params):
        cmd = "ubertooth-specan"
        if mode == "BT":
            cmd += " -b"
        elif mode == "CUSTOM":
            cmd += f" -s {params[0]} -e {params[1]} -l {params[2]}"
        
        print("\nStarting spectrum analysis...")
        run_command(cmd)
    
    def spectrum_monitor(self):
        print("\nStarting continuous spectrum monitoring...")
        run_command("ubertooth-specan -l 0")
    
    def channel_utilization(self):
        print("\nMeasuring channel utilization...")
        output = run_command("ubertooth-util -c", capture_output=True)
        if output:
            print(output)
            save_to_file(output, "channel_utilization")
    
    def transmit_packets(self, mode, *params):
        cmd = "ubertooth-tx"
        if mode == "CUSTOM":
            cmd += f" -c {params[0]} -d {params[1]}"
        
        print("\nStarting packet transmission...")
        run_command(cmd)
    
    def jam(self, mode, param):
        cmd = "ubertooth-jam"
        if mode == "CHANNEL":
            cmd += f" -c {param}"
        elif mode == "DEVICE":
            cmd += f" -t {param}"
        
        print("\nStarting jamming operation...")
        run_command(cmd)
    
    def discover_devices(self, mode):
        cmd = "ubertooth-scan" if mode == "CLASSIC" else "ubertooth-btle -s"
        print(f"\nDiscovering {mode} devices...")
        output = run_command(cmd, capture_output=True)
        if output:
            print(output)
            save_to_file(output, f"{mode.lower()}_discovery")
    
    def monitor_rssi(self):
        print("\nMonitoring RSSI values...")
        run_command("ubertooth-rssi")
    
    def continuous_monitoring(self):
        print("\nStarting continuous device monitoring...")
        run_command("ubertooth-scan -c")
    
    def show_ubertooth_info(self):
        print("\nUbertooth Device Information:")
        run_command("ubertooth-util -v")
        run_command("ubertooth-util -s")
        input("\nPress Enter to continue...")
    
    def update_firmware(self):
        print("\nUpdating Ubertooth firmware...")
        run_command("ubertooth-dfu -d bluetooth_rxtx.dfu -U")
    
    def reset_ubertooth(self):
        print("\nResetting Ubertooth...")
        run_command("ubertooth-util -r")
    
    def check_usb(self):
        print("\nChecking USB connection...")
        run_command("lsusb -d 1d50:6002")
        input("\nPress Enter to continue...")
    
    def pin_cracking(self):
        print("\nThis feature requires additional setup with tools like crackle")
        print("Would you like to attempt Bluetooth PIN cracking? (y/n)")
        choice = input().lower()
        if choice == 'y':
            run_command("crackle -i capture.pcap -o output.pcap")
    
    def capture_pairing(self):
        print("\nCapturing BLE pairing process...")
        print("Put target devices in pairing mode")
        run_command("ubertooth-btle -p")
    
    def load_custom_fpga(self):
        print("\nLoading custom FPGA image...")
        file = input("Enter path to FPGA image: ")
        if os.path.exists(file):
            run_command(f"ubertooth-util -U {file}")
        else:
            print("File not found")
    
    def capture_pcap(self, mode):
        filename = f"capture_{mode.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
        cmd = f"ubertooth-btle -f -c {filename}" if mode == "BLE" else f"ubertooth-bt -c {filename}"
        print(f"\nCapturing {mode} traffic to {filename}...")
        run_command(cmd)
    
    def realtime_decode(self, mode):
        cmd = "ubertooth-btle -f -D" if mode == "BLE" else "ubertooth-bt -D"
        print(f"\nStarting real-time {mode} decoding...")
        run_command(cmd)
    
    def main_loop(self):
        while self.running:
            self.show_menu()
            choice = input("Select option: ")
            
            if choice == "1":
                self.bluetooth_classic_menu()
            elif choice == "2":
                self.ble_menu()
            elif choice == "3":
                self.spectrum_menu()
            elif choice == "4":
                self.transmission_menu()
            elif choice == "5":
                self.discovery_menu()
            elif choice == "6":
                self.utilities_menu()
            elif choice == "7":
                self.advanced_menu()
            elif choice == "0":
                print("\nExiting Ubertooth Tool...")
                self.running = False
            else:
                print("Invalid selection, please try again")
                time.sleep(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This tool requires root privileges. Please run with sudo.")
        sys.exit(1)
    
    tool = UbertoothTool()
    tool.main_loop()
