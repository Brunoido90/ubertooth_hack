Ubertooth One – Complete GUI Control
A feature‑complete graphical interface for the Ubertooth One Bluetooth development platform. This tool wraps every real ubertooth-util command into a clean Tkinter GUI – no fictional attacks, no broken subcommands, no silent failures.

Features
All hardware‑supported operations – sniffing, scanning, monitoring, analysis, firmware management.
Dynamic argument fields – duration for captures, file path for replay/upgrade, shown only when needed.
Threaded execution – GUI stays responsive during long operations.
Real‑time output – scrollable log with timestamps.
Error‑resistant – validates root, device presence, firmware, and all user inputs before running.
Safe defaults – no automatic DFU mode; DFU is a separate explicit command.
Requirements
Python 3.6+
tkinter (usually included with Python)
ubertooth-util installed and in $PATH
Root privileges (sudo)
Ubertooth One device connected via USB
Installation
bash
Wrap
Copy
git clone <repo-url>

cd ubertooth-gui

# No extra Python dependencies – uses only standard library.
Usage
bash
Wrap
Copy
sudo python3 ubertooth_complete_gui.py
Select a command from the dropdown.
If the command requires a duration or file path, the corresponding field appears automatically.
Click Execute – output streams into the log window.
Click Stop to abort (note: the underlying process cannot be killed cleanly; it will run until completion or timeout).
Available Commands
Command	Arguments	Description
Classic Sniff	duration (s)	Capture Classic Bluetooth packets
LE Sniff	duration (s)	Capture Bluetooth Low Energy packets
HCI Capture	duration (s)	Capture HCI traffic
Replay HCI Capture	file path	Replay a previously captured HCI file
Start Monitor Mode	none	Enable monitor mode (continuous capture)
Stop Monitor Mode	none	Disable monitor mode
Analyze Classic Data	none	Analyse captured Classic data (requires prior capture file)
Analyze LE Data	none	Analyse captured LE data (requires prior capture file)
Classic Inquiry	none	Discover nearby Classic Bluetooth devices
LE Scan	none	Scan for BLE advertisements
Enter DFU Mode	none	Put device into DFU mode (for firmware upgrade)
Firmware Upgrade	file path (.bin)	Flash new firmware onto the device
What This Tool Does NOT Do
The Ubertooth One hardware is a sniffer/analyzer, not a full Bluetooth stack. The following attack types are not supported by ubertooth-util and are therefore not included:

Device pairing, unpairing, or connection management
MAC address spoofing
Man‑in‑the‑middle attacks
Bluesnarfing, bluejacking, bluebugging
WhisperPair, Magic Keyboard, BleedingTooth
Passkey or Just Works spoofing
These require other tools (e.g., btlejack, bettercap, internalblue).

Troubleshooting
"No Ubertooth One device found"

Ensure the device is plugged in.
Check lsusb for 1d50:6002 (Ubertooth One) or 1d50:6003 (Ubertooth Zero).
Try re‑plugging or resetting the device (press the reset button).
"Command failed (rc=...)"

Verify the device is in normal mode (not DFU). If you entered DFU mode earlier, power‑cycle the device.
Check that ubertooth-util is installed: which ubertooth-util
Run the command manually in a terminal to see the full error: sudo ubertooth-util -d /dev/ttyACM0 <subcommand>
"Firmware: UNKNOWN"

The device may have corrupted firmware. Re‑flash using the Firmware Upgrade command with a valid .bin file from the official Ubertooth releases.
License
This tool is provided for educational and authorized security testing purposes only. Use at your own risk. The authors assume no liability for misuse.
