#!/usr/bin/env python3
"""
Ubertooth One – Complete GUI Tool
All real ubertooth-util commands, no fictional attacks.
Requires root and a connected Ubertooth One device.
"""
import subprocess
import os
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime

class UbertoothUtils:
    @staticmethod
    def run(cmd: list, timeout: int = 30) -> tuple:
        """Returns (stdout, returncode). On failure stdout contains error."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode != 0:
                return (result.stderr.strip(), result.returncode)
            return (result.stdout.strip(), 0)
        except subprocess.TimeoutExpired:
            return ("Command timed out", -1)
        except Exception as e:
            return (str(e), -2)

    @staticmethod
    def require_root():
        if os.geteuid() != 0:
            raise RuntimeError("Root privileges required (sudo)")

    @staticmethod
    def get_device() -> str:
        if os.path.exists('/dev/ttyACM0'):
            return '/dev/ttyACM0'
        raise RuntimeError("No Ubertooth One device found on /dev/ttyACM0")

    @staticmethod
    def get_firmware_version() -> str:
        out, rc = UbertoothUtils.run(["ubertooth-util", "-v"])
        if rc != 0:
            raise RuntimeError(f"Failed to query firmware: {out}")
        return out

class UbertoothGUI:
    # Real ubertooth-util commands with their argument requirements
    COMMANDS = {
        "Classic Sniff": {"args": ["duration"], "cmd": ["ubertooth-util", "-d", "DEVICE", "classic", "sniff", "-t", "DURATION"]},
        "LE Sniff":      {"args": ["duration"], "cmd": ["ubertooth-util", "-d", "DEVICE", "le", "sniff", "-t", "DURATION"]},
        "HCI Capture":   {"args": ["duration"], "cmd": ["ubertooth-util", "-d", "DEVICE", "hci", "capture", "-t", "DURATION"]},
        "Replay HCI Capture": {"args": ["file"], "cmd": ["ubertooth-util", "-d", "DEVICE", "hci", "replay", "FILE"]},
        "Start Monitor Mode":  {"args": [], "cmd": ["ubertooth-util", "-d", "DEVICE", "monitor"]},
        "Stop Monitor Mode":   {"args": [], "cmd": ["ubertooth-util", "-d", "DEVICE", "monitor", "stop"]},
        "Analyze Classic Data": {"args": [], "cmd": ["ubertooth-util", "-d", "DEVICE", "classic", "analyze"]},
        "Analyze LE Data":      {"args": [], "cmd": ["ubertooth-util", "-d", "DEVICE", "le", "analyze"]},
        "Classic Inquiry":      {"args": [], "cmd": ["ubertooth-util", "-d", "DEVICE", "classic", "inquiry"]},
        "LE Scan":              {"args": [], "cmd": ["ubertooth-util", "-d", "DEVICE", "le", "scan"]},
        "Enter DFU Mode":       {"args": [], "cmd": ["ubertooth-util", "-d", "DEVICE", "dfu"]},
        "Firmware Upgrade":     {"args": ["file"], "cmd": ["ubertooth-util", "-d", "DEVICE", "-U", "FILE"]},
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Ubertooth One – Complete Control")
        self.root.geometry("800x650")
        self.running = False
        self.current_process = None  # not used, but for future kill

        # Status bar
        self.status_var = tk.StringVar(value="Initializing...")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Main frame
        main_frame = ttk.Frame(root, padding=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Device info
        info_frame = ttk.LabelFrame(main_frame, text="Device", padding=5)
        info_frame.pack(fill=tk.X, pady=5)
        self.device_label = ttk.Label(info_frame, text="Device: checking...")
        self.device_label.pack(side=tk.LEFT, padx=5)
        self.fw_label = ttk.Label(info_frame, text="Firmware: checking...")
        self.fw_label.pack(side=tk.LEFT, padx=5)

        # Command selection
        ctrl_frame = ttk.LabelFrame(main_frame, text="Command", padding=5)
        ctrl_frame.pack(fill=tk.X, pady=5)

        ttk.Label(ctrl_frame, text="Select command:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.cmd_var = tk.StringVar()
        self.cmd_combo = ttk.Combobox(ctrl_frame, textvariable=self.cmd_var, state="readonly", width=45)
        self.cmd_combo['values'] = list(self.COMMANDS.keys())
        self.cmd_combo.current(0)
        self.cmd_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.cmd_combo.bind('<<ComboboxSelected>>', self.on_command_change)

        # Dynamic argument fields
        self.args_frame = ttk.Frame(ctrl_frame)
        self.args_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.duration_label = ttk.Label(self.args_frame, text="Duration (seconds):")
        self.duration_entry = ttk.Entry(self.args_frame, width=10)
        self.duration_var = tk.StringVar(value="120")

        self.file_label = ttk.Label(self.args_frame, text="File path:")
        self.file_entry = ttk.Entry(self.args_frame, width=40)
        self.file_var = tk.StringVar()

        # Buttons
        btn_frame = ttk.Frame(ctrl_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.start_btn = ttk.Button(btn_frame, text="Execute", command=self.start_command)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_command, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Output", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=14, state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Initialize device
        self.init_device()
        self.on_command_change()  # show initial args

    def log(self, msg: str, level: str = "INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{level}] {msg}\n"
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, line)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def init_device(self):
        try:
            UbertoothUtils.require_root()
            device = UbertoothUtils.get_device()
            fw = UbertoothUtils.get_firmware_version()
            self.device_label.config(text=f"Device: {device}")
            self.fw_label.config(text=f"Firmware: {fw}")
            self.log("Device ready.", "INFO")
            self.status_var.set("Ready")
        except Exception as e:
            self.device_label.config(text="Device: NOT FOUND")
            self.fw_label.config(text="Firmware: UNKNOWN")
            self.log(f"Initialization failed: {e}", "ERROR")
            messagebox.showerror("Device Error", str(e))
            self.start_btn.config(state=tk.DISABLED)
            self.status_var.set("Error")

    def on_command_change(self, event=None):
        cmd_name = self.cmd_var.get()
        info = self.COMMANDS.get(cmd_name, {})
        args = info.get("args", [])

        # Hide all fields first
        self.duration_label.pack_forget()
        self.duration_entry.pack_forget()
        self.file_label.pack_forget()
        self.file_entry.pack_forget()

        if "duration" in args:
            self.duration_label.pack(side=tk.LEFT, padx=5)
            self.duration_entry.pack(side=tk.LEFT, padx=5)
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, self.duration_var.get())
        if "file" in args:
            self.file_label.pack(side=tk.LEFT, padx=5)
            self.file_entry.pack(side=tk.LEFT, padx=5)
            self.file_entry.delete(0, tk.END)

    def start_command(self):
        if self.running:
            return
        cmd_name = self.cmd_var.get()
        if not cmd_name:
            return

        # Build command
        info = self.COMMANDS.get(cmd_name)
        if not info:
            self.log(f"Unknown command: {cmd_name}", "ERROR")
            return

        device = '/dev/ttyACM0'
        cmd_template = info["cmd"]
        args_needed = info["args"]

        # Replace placeholders
        cmd = []
        for part in cmd_template:
            if part == "DEVICE":
                cmd.append(device)
            elif part == "DURATION":
                try:
                    d = int(self.duration_var.get().strip())
                    if d <= 0:
                        raise ValueError
                except:
                    self.log("Duration must be a positive integer.", "ERROR")
                    return
                cmd.append(str(d))
            elif part == "FILE":
                f = self.file_var.get().strip()
                if not f:
                    self.log("File path required.", "ERROR")
                    return
                cmd.append(f)
            else:
                cmd.append(part)

        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Running: {cmd_name}...")
        self.log(f"Executing: {' '.join(cmd)}", "INFO")

        # Determine timeout: duration + 10 for sniff/capture, else 30
        if "duration" in args_needed:
            timeout = int(cmd[cmd.index("-t")+1]) + 10 if "-t" in cmd else 30
        else:
            timeout = 30

        self.thread = threading.Thread(target=self._run, args=(cmd, timeout), daemon=True)
        self.thread.start()

    def _run(self, cmd: list, timeout: int):
        try:
            out, rc = UbertoothUtils.run(cmd, timeout=timeout)
            if rc != 0:
                self.log(f"Command failed (rc={rc}): {out[:500]}", "ERROR")
            else:
                if out:
                    self.log(f"Output:\n{out[:1000]}", "INFO")
                else:
                    self.log("Command completed (no output)", "INFO")
        except Exception as e:
            self.log(f"Unexpected error: {e}", "ERROR")
        finally:
            self.root.after(0, self._finished)

    def _finished(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Ready")

    def stop_command(self):
        if self.running:
            self.log("Stop requested – cannot kill subprocess gracefully; command may continue.", "WARN")
            self.running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_var.set("Stopped (may still run)")

if __name__ == "__main__":
    root = tk.Tk()
    app = UbertoothGUI(root)
    root.mainloop()
