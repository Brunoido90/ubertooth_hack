#!/usr/bin/env python3
import subprocess
import os
import time
from datetime import datetime

class Logger:
    @staticmethod
    def log(msg: str, level: str = "INFO"):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\033[92m[{ts}] [{level}]\033[0m {msg}")

class UbertoothUtils:
    @staticmethod
    def run(cmd: list, timeout: int = 15) -> str:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout.strip()
        except Exception as e:
            Logger.log(str(e), "ERROR")
            return ""

    @staticmethod
    def require_root():
        if os.geteuid() != 0:
            Logger.log("\033[91mRoot-Rechte erforderlich (sudo)\033[0m", "ERROR")
            exit(1)

    @staticmethod
    def get_ubertooth_device():
        try:
            # Überprüfen, ob das Gerät unter /dev/ttyACM0 erkannt wird
            if os.path.exists('/dev/ttyACM0'):
                return '/dev/ttyACM0'
            else:
                Logger.log("\033[91mKein Ubertooth One Gerät gefunden\033[0m", "ERROR")
                exit(1)
        except Exception as e:
            Logger.log(str(e), "ERROR")
            exit(1)

    @staticmethod
    def check_ubertooth_firmware():
        try:
            firmware_version = UbertoothUtils.run(["ubertooth-util", "-v"])
            Logger.log(f"\033[94mUbertooth Firmware Version: {firmware_version}\033[0m")
        except Exception as e:
            Logger.log(str(e), "ERROR")
            exit(1)

    @staticmethod
    def enter_dfu_mode():
        try:
            Logger.log("\033[94mVersuche, das Ubertooth One Gerät in den DFU-Modus zu versetzen...\033[0m")
            UbertoothUtils.run(["ubertooth-util", "dfu"])
            Logger.log("\033[94mDFU-Modus erfolgreich aktiviert\033[0m")
        except Exception as e:
            Logger.log(str(e), "ERROR")
            Logger.log("\033[91mKonnte das Gerät nicht in den DFU-Modus versetzen\033[0m", "ERROR")

class UbertoothOneTools:
    def __init__(self):
        self.device = UbertoothUtils.get_ubertooth_device()
        UbertoothUtils.check_ubertooth_firmware()
        UbertoothUtils.enter_dfu_mode()

    def classic_sniff(self, duration: int = 120):
        Logger.log(f"\033[94mClassic Sniff ({duration}s)\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "sniff", "-t", str(duration)])
        time.sleep(duration)
        Logger.log("\033[94mSniff completed\033[0m")

    def le_sniff(self, duration: int = 120):
        Logger.log(f"\033[94mLE Sniff ({duration}s)\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "sniff", "-t", str(duration)])
        time.sleep(duration)
        Logger.log("\033[94mSniff completed\033[0m")

    def hci_capture(self, duration: int = 120):
        Logger.log(f"\033[94mHCI Capture ({duration}s)\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "hci", "capture", "-t", str(duration)])
        time.sleep(duration)
        Logger.log("\033[94mCapture completed\033[0m")

    def hci_replay(self, file_path: str):
        Logger.log(f"\033[94mReplaying HCI capture from {file_path}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "hci", "replay", file_path])

    def monitor_mode(self):
        Logger.log("\033[94mStarting monitor mode\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "monitor"])

    def stop_monitor_mode(self):
        Logger.log("\033[94mStopping monitor mode\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "monitor", "stop"])

    def classic_analyze(self):
        Logger.log("\033[94mAnalyzing captured classic data\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "analyze"])

    def le_analyze(self):
        Logger.log("\033[94mAnalyzing captured LE data\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "analyze"])

    def classic_connection(self, mac: str):
        Logger.log(f"\033[94mConnecting to classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "connect", mac])

    def le_connection(self, mac: str):
        Logger.log(f"\033[94mConnecting to LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "connect", mac])

    def classic_disconnect(self, mac: str):
        Logger.log(f"\033[94mDisconnecting from classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "disconnect", mac])

    def le_disconnect(self, mac: str):
        Logger.log(f"\033[94mDisconnecting from LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "disconnect", mac])

    def classic_pair(self, mac: str):
        Logger.log(f"\033[94mPairing with classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "pair", mac])

    def le_pair(self, mac: str):
        Logger.log(f"\033[94mPairing with LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "pair", mac])

    def classic_unpair(self, mac: str):
        Logger.log(f"\033[94mUnpairing from classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "unpair", mac])

    def le_unpair(self, mac: str):
        Logger.log(f"\033[94mUnpairing from LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "unpair", mac])

    def classic_inquiry(self):
        Logger.log("\033[94mPerforming classic inquiry\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "inquiry"])

    def le_scan(self):
        Logger.log("\033[94mPerforming LE scan\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "scan"])

    def classic_spoof(self, mac: str):
        Logger.log(f"\033[94mSpoofing classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "spoof", mac])

    def le_spoof(self, mac: str):
        Logger.log(f"\033[94mSpoofing LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "spoof", mac])

    def classic_man_in_the_middle(self, mac: str):
        Logger.log(f"\033[94mPerforming Man-in-the-Middle attack on classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "mitm", mac])

    def le_man_in_the_middle(self, mac: str):
        Logger.log(f"\033[94mPerforming Man-in-the-Middle attack on LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "mitm", mac])

    def classic_passkey_spoofing(self, mac: str, passkey: str):
        Logger.log(f"\033[94mPerforming Passkey Spoofing on classic device {mac} with passkey {passkey}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "passkey", mac, passkey])

    def le_passkey_spoofing(self, mac: str, passkey: str):
        Logger.log(f"\033[94mPerforming Passkey Spoofing on LE device {mac} with passkey {passkey}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "passkey", mac, passkey])

    def classic_just_works_spoofing(self, mac: str):
        Logger.log(f"\033[94mPerforming Just Works Spoofing on classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "justworks", mac])

    def le_just_works_spoofing(self, mac: str):
        Logger.log(f"\033[94mPerforming Just Works Spoofing on LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "justworks", mac])

    def classic_bluesnarfing(self, mac: str):
        Logger.log(f"\033[94mPerforming Bluesnarfing attack on classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "bluesnarf", mac])

    def le_bluesnarfing(self, mac: str):
        Logger.log(f"\033[94mPerforming Bluesnarfing attack on LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "bluesnarf", mac])

    def classic_bluejacking(self, mac: str, message: str):
        Logger.log(f"\033[94mPerforming Bluejacking attack on classic device {mac} with message: {message}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "bluejack", mac, message])

    def le_bluejacking(self, mac: str, message: str):
        Logger.log(f"\033[94mPerforming Bluejacking attack on LE device {mac} with message: {message}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "bluejack", mac, message])

    def classic_bluebugging(self, mac: str):
        Logger.log(f"\033[94mPerforming Bluebugging attack on classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "bluebug", mac])

    def le_bluebugging(self, mac: str):
        Logger.log(f"\033[94mPerforming Bluebugging attack on LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "bluebug", mac])

    def classic_whisperpair(self, mac: str):
        Logger.log(f"\033[94mPerforming WhisperPair attack on classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "whisperpair", mac])

    def le_whisperpair(self, mac: str):
        Logger.log(f"\033[94mPerforming WhisperPair attack on LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "whisperpair", mac])

    def classic_magic_keyboard(self, mac: str):
        Logger.log(f"\033[94mPerforming Magic Keyboard attack on classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "magickeyboard", mac])

    def le_magic_keyboard(self, mac: str):
        Logger.log(f"\033[94mPerforming Magic Keyboard attack on LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "magickeyboard", mac])

    def classic_bleedingtooth(self, mac: str):
        Logger.log(f"\033[94mPerforming BleedingTooth attack on classic device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "classic", "bleedingtooth", mac])

    def le_bleedingtooth(self, mac: str):
        Logger.log(f"\033[94mPerforming BleedingTooth attack on LE device {mac}\033[0m")
        UbertoothUtils.run(["ubertooth-util", "-d", self.device, "le", "bleedingtooth", mac])

def main():
    UbertoothUtils.require_root()
    tools = UbertoothOneTools()

    while True:
        print("\n\033[93m1) Classic Sniff\033[0m")
        print("\033[93m2) LE Sniff\033[0m")
        print("\033[93m3) HCI Capture\033[0m")
        print("\033[93m4) Replay HCI Capture\033[0m")
        print("\033[93m5) Start Monitor Mode\033[0m")
        print("\033[93m6) Stop Monitor Mode\033[0m")
        print("\033[93m7) Analyze Classic Data\033[0m")
        print("\033[93m8) Analyze LE Data\033[0m")
        print("\033[93m9) Connect to Classic Device\033[0m")
        print("\033[93m10) Connect to LE Device\033[0m")
        print("\033[93m11) Disconnect from Classic Device\033[0m")
        print("\033[93m12) Disconnect from LE Device\033[0m")
        print("\033[93m13) Pair with Classic Device\033[0m")
        print("\033[93m14) Pair with LE Device\033[0m")
        print("\033[93m15) Unpair from Classic Device\033[0m")
        print("\033[93m16) Unpair from LE Device\033[0m")
        print("\033[93m17) Classic Inquiry\033[0m")
        print("\033[93m18) LE Scan\033[0m")
        print("\033[93m19) Spoof Classic Device\033[0m")
        print("\033[93m20) Spoof LE Device\033[0m")
        print("\033[93m21) Man-in-the-Middle Attack on Classic\033[0m")
        print("\033[93m22) Man-in-the-Middle Attack on LE\033[0m")
        print("\033[93m23) Passkey Spoofing on Classic\033[0m")
        print("\033[93m24) Passkey Spoofing on LE\033[0m")
        print("\033[93m25) Just Works Spoofing on Classic\033[0m")
        print("\033[93m26) Just Works Spoofing on LE\033[0m")
        print("\033[93m27) Bluesnarfing on Classic\033[0m")
        print("\033[93m28) Bluesnarfing on LE\033[0m")
        print("\033[93m29) Bluejacking on Classic\033[0m")
        print("\033[93m30) Bluejacking on LE\033[0m")
        print("\033[93m31) Bluebugging on Classic\033[0m")
        print("\033[93m32) Bluebugging on LE\033[0m")
        print("\033[93m33) WhisperPair Attack on Classic\033[0m")
        print("\033[93m34) WhisperPair Attack on LE\033[0m")
        print("\033[93m35) Magic Keyboard Attack on Classic\033[0m")
        print("\033[93m36) Magic Keyboard Attack on LE\033[0m")
        print("\033[93m37) BleedingTooth Attack on Classic\033[0m")
        print("\033[93m38) BleedingTooth Attack on LE\033[0m")
        print("\033[93m39) Exit\033[0m")
        c = input("\033[96m> \033[0m").strip()

        if c == "1":
            duration = int(input("\033[96mDauer des Sniffs (Sekunden): \033[0m").strip())
            tools.classic_sniff(duration)
        elif c == "2":
            duration = int(input("\033[96mDauer des Sniffs (Sekunden): \033[0m").strip())
            tools.le_sniff(duration)
        elif c == "3":
            duration = int(input("\033[96mDauer der HCI Capture (Sekunden): \033[0m").strip())
            tools.hci_capture(duration)
        elif c == "4":
            file_path = input("\033[96mPfad zur HCI Capture Datei: \033[0m").strip()
            tools.hci_replay(file_path)
        elif c == "5":
            tools.monitor_mode()
        elif c == "6":
            tools.stop_monitor_mode()
        elif c == "7":
            tools.classic_analyze()
        elif c == "8":
            tools.le_analyze()
        elif c == "9":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_connection(mac)
        elif c == "10":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_connection(mac)
        elif c == "11":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_disconnect(mac)
        elif c == "12":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_disconnect(mac)
        elif c == "13":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_pair(mac)
        elif c == "14":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_pair(mac)
        elif c == "15":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_unpair(mac)
        elif c == "16":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_unpair(mac)
        elif c == "17":
            tools.classic_inquiry()
        elif c == "18":
            tools.le_scan()
        elif c == "19":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_spoof(mac)
        elif c == "20":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_spoof(mac)
        elif c == "21":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_man_in_the_middle(mac)
        elif c == "22":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_man_in_the_middle(mac)
        elif c == "23":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            passkey = input("\033[96mPasskey: \033[0m").strip()
            tools.classic_passkey_spoofing(mac, passkey)
        elif c == "24":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            passkey = input("\033[96mPasskey: \033[0m").strip()
            tools.le_passkey_spoofing(mac, passkey)
        elif c == "25":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_just_works_spoofing(mac)
        elif c == "26":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_just_works_spoofing(mac)
        elif c == "27":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_bluesnarfing(mac)
        elif c == "28":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_bluesnarfing(mac)
        elif c == "29":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            message = input("\033[96mNachricht: \033[0m").strip()
            tools.classic_bluejacking(mac, message)
        elif c == "30":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            message = input("\033[96mNachricht: \033[0m").strip()
            tools.le_bluejacking(mac, message)
        elif c == "31":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_bluebugging(mac)
        elif c == "32":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_bluebugging(mac)
        elif c == "33":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_whisperpair(mac)
        elif c == "34":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_whisperpair(mac)
        elif c == "35":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_magic_keyboard(mac)
        elif c == "36":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_magic_keyboard(mac)
        elif c == "37":
            mac = input("\033[96mMAC-Adresse des Classic Geräts: \033[0m").strip()
            tools.classic_bleedingtooth(mac)
        elif c == "38":
            mac = input("\033[96mMAC-Adresse des LE Geräts: \033[0m").strip()
            tools.le_bleedingtooth(mac)
        elif c == "39":
            print("\033[92mExiting...\033[0m")
            break
        else:
            Logger.log("\033[91mUngültige Option\033[0m", "ERROR")

if __name__ == "__main__":
    main()
