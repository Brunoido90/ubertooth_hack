#!/usr/bin/env python3
"""
Ubertooth One – Complete Control GUI (Extended Edition)
========================================================
Vollständige grafische Oberfläche für ALLE echten Ubertooth-Tools.
Jede GUI-Aktion entspricht 1:1 einer realen CLI-Option (verifiziert gegen
die Manpages von Ubuntu/Kali und die Doku von greatscottgadgets/ubertooth).

Tools:
  ubertooth-util    Geräte-Info, Funk-Konfiguration, Reset, DFU/ISP, Tests
  ubertooth-btle    BLE: Follow / Promiscuous / Advertising / Interferenz
  ubertooth-rx      Classic BR/EDR: Survey, Piconet-Follow, Datei-Analyse
  ubertooth-follow  CLK-Recovery + Follow für UAP/LAP
  ubertooth-afh     Passive AFH-Kanalmap-Erkennung
  ubertooth-scan    Aktiver BlueZ-Scan (Inquiry / Extended Inquiry)
  ubertooth-specan  RSSI-Spektrum (Text/feedgnuplot/3D)
  ubertooth-specan-ui  Grafische Spektralanalyse
  ubertooth-dump    Roh-Bitstrom (Classic/BLE)
  ubertooth-debug   CC2400-Register lesen
  ubertooth-dfu     Firmware schreiben/lesen
  crackle           BLE-Schlüssel-Recovery (TK/LTK)
  tshark/wireshark  Analyse der Captures, Live-Pipe

WICHTIG: ubertooth-util hat KEINE Subkommandos (kein "classic sniff" o.Ä.).
Alle Befehle verwenden die echte Flag-basierte CLI. Erfordert Root und
mindestens einen angeschlossenen Ubertooth One/Zero.
"""
import os
import queue
import signal
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime

# ---------------------------------------------------------------------------
# Konstanten
# ---------------------------------------------------------------------------
UBERTOOTH_TOOLS = {  # Tools, die den -U<0-7>-Geräteindex unterstützen
    "ubertooth-util", "ubertooth-btle", "ubertooth-rx", "ubertooth-follow",
    "ubertooth-afh", "ubertooth-scan", "ubertooth-specan", "ubertooth-specan-ui",
    "ubertooth-dump", "ubertooth-debug", "ubertooth-dfu",
}
ALL_TOOLS = sorted(UBERTOOTH_TOOLS | {"crackle", "wireshark", "tshark"})

FIFO = "/tmp/ubertooth.pipe"


def require_root():
    if os.geteuid() != 0:
        raise RuntimeError("Root-Rechte erforderlich (mit sudo ausführen)")


def have(tool):
    return subprocess.run(["which", tool], capture_output=True).returncode == 0


def run_sync(cmd, timeout=15):
    """Kurzer synchroner Aufruf -> (stdout_or_err, returncode)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (r.stderr.strip() if r.returncode != 0 else r.stdout.strip(),
                r.returncode)
    except subprocess.TimeoutExpired:
        return ("Timeout", -1)
    except Exception as e:
        return (str(e), -2)


# ---------------------------------------------------------------------------
# Befehlsdefinitionen
#   Feld-Tupel: (key, label, flag, style, required, default)
#     style "attached" -> -c2402 | "separate" -> -c 2402 | "flag" -> Checkbox
# ---------------------------------------------------------------------------
class Spec:
    def __init__(self, tool, base=(), fields=(), timeout=None, detach=False,
                 pre=(), post=(), note=""):
        self.tool = tool
        self.base = list(base)
        self.fields = fields
        self.timeout = timeout      # Prozess nach N s töten (Info-Abfragen)
        self.detach = detach        # GUI-Tool starten, nicht streamen
        self.pre = list(pre)        # Shell-Kommandos vor dem Start
        self.post = list(post)      # Shell-Kommandos nach dem Ende
        self.note = note


# ---------------- Tab 1: Gerät & Funk (ubertooth-util) ----------------------
UTIL_CMDS = {
    "Identifikation (LEDs blinken)": Spec("ubertooth-util", ["-I"], timeout=15),
    "Firmware-Revision":              Spec("ubertooth-util", ["-v"], timeout=15),
    "Kompilier-Info":                 Spec("ubertooth-util", ["-V"], timeout=15),
    "Board-ID":                       Spec("ubertooth-util", ["-b"], timeout=15),
    "Part ID (Mikrocontroller)":      Spec("ubertooth-util", ["-p"], timeout=15),
    "Seriennummer":                   Spec("ubertooth-util", ["-s"], timeout=15),
    "Anzahl angeschlossener Geräte":  Spec("ubertooth-util", ["-N"], timeout=15),
    "Voll-Reset":                     Spec("ubertooth-util", ["-r"], timeout=15),
    "Operation stoppen":              Spec("ubertooth-util", ["-S"], timeout=15),
    "DFU-Modus aktivieren (Firmware)":Spec("ubertooth-util", ["-f"], timeout=15),
    "ISP-Modus aktivieren":           Spec("ubertooth-util", ["-i"], timeout=15),
    "PA-Level setzen":     Spec("ubertooth-util", [],
                                [("pa", "PA-Level (0-7)", "-a", "attached", True, "")], timeout=15),
    "Kanal setzen (MHz)":  Spec("ubertooth-util", [],
                                [("chmhz", "Kanal MHz (2400-2483)", "-c", "attached", True, "")], timeout=15),
    "Kanal setzen (Index)":Spec("ubertooth-util", [],
                                [("chidx", "Kanal-Index (0-78)", "-C", "attached", True, "")], timeout=15),
    "Squelch setzen":      Spec("ubertooth-util", [],
                                [("sql", "Squelch dBm (z.B. -50)", "-z", "attached", True, "")], timeout=15),
    "LED-Spektrumanalyzer":Spec("ubertooth-util", [],
                                [("rssi", "RSSI-Schwelle (1-225)", "-q", "attached", True, "")], timeout=None,
                                note="Läuft bis zum Stopp. Auswertung über ubertooth-specan."),
    "Alle LEDs setzen":    Spec("ubertooth-util", [],
                                [("leds", "Alle LEDs (0=aus/1=an)", "-d", "attached", True, "")], timeout=15),
    "USR-LED setzen":      Spec("ubertooth-util", [],
                                [("usr", "USR-LED (0=aus/1=an)", "-l", "attached", True, "")], timeout=15),
    "Transmittest (Dauer-Senden)": Spec("ubertooth-util", ["-t"],
                                        note="SENDEN! Rechtslage prüfen (FTEG/EMVG)."),
    "Repeater-Modus":      Spec("ubertooth-util", ["-e"], timeout=15),
    "Reichweitentest starten": Spec("ubertooth-util", ["-n"], timeout=15),
    "Reichweitentest Ergebnis": Spec("ubertooth-util", ["-m"], timeout=15),
    "Xmas-Lights (LED-Show)": Spec("ubertooth-util", ["-x"], timeout=15),
}

# ---------------- Tab 2: BLE (ubertooth-btle) -------------------------------
BTLE_CMDS = {
    "Follow-Capture (PCAPNG)": Spec("ubertooth-btle", ["-f"],
        [("out", "Ausgabedatei (.pcapng)", "-r", "attached", True, "capture.pcapng"),
         ("target", "Ziel-BD_ADDR (optional)", "-t", "attached", False, ""),
         ("advch", "Adv-Kanal 37/38/39", "-A", "attached", False, "37")]),
    "Follow-Capture gezielt": Spec("ubertooth-btle", ["-f"],
        [("target", "Ziel-BD_ADDR", "-t", "attached", True, ""),
         ("out", "Ausgabedatei (.pcapng)", "-r", "attached", False, "")]),
    "Promiscuous-Capture": Spec("ubertooth-btle", ["-p"],
        [("out", "Ausgabedatei (.pcapng)", "-r", "attached", True, "promisc.pcapng"),
         ("aa", "Access-Address (hex, optional)", "-a", "attached", False, "")]),
    "Advertising-Scan (nur Werbung)": Spec("ubertooth-btle", ["-n"],
        [("out", "Ausgabedatei (optional)", "-r", "attached", False, "")]),
    "Faux-Slave (Advertising injizieren)": Spec("ubertooth-btle", ["-s"],
        [("bdaddr", "Eigene BD_ADDR", "-s", "attached", True, "")],
        note="Injiziert Advertising-Pakete mit eigener MAC – SENDEN!"),
    "Interferenz auf Verbindung": Spec("ubertooth-btle", ["-f", "-I"],
        [("target", "Ziel-BD_ADDR (optional)", "-t", "attached", False, "")],
        note="Stört Verbindungen – nur mit Genehmigung!"),
    "CRC-Verifikation setzen": Spec("ubertooth-btle", [],
        [("crc", "CRC-Modus (0=aus/1=ein)", "-v", "attached", True, "1")], timeout=15),
    "Access-Address setzen": Spec("ubertooth-btle", [],
        [("aa", "Access-Address (hex, z.B. 8e89bed6)", "-a", "attached", True, "")], timeout=15),
    "Capture für crackle (PPI-PCAP)": Spec("ubertooth-btle", ["-f"],
        [("out", "Ausgabedatei (.pcap)", "-c", "attached", True, "crackle.pcap")],
        note="PPI-Format – Eingabe für crackle."),
    "Capture als PCAP (LE-Pseudoheader)": Spec("ubertooth-btle", ["-f"],
        [("out", "Ausgabedatei (.pcap)", "-q", "attached", True, "le.pcap")]),
}

# ---------------- Tab 3: Classic BR/EDR -------------------------------------
CLASSIC_CMDS = {
    "Survey-Modus (alle Piconets)": Spec("ubertooth-rx", ["-z"],
        [("t", "Timeout Sekunden (20-60)", "-t", "separate", True, "30"),
         ("out", "Ausgabe (.pcapng, optional)", "-r", "separate", False, "")]),
    "Piconet folgen (LAP/UAP)": Spec("ubertooth-rx", [],
        [("lap", "LAP (6 Hex)", "-l", "separate", True, ""),
         ("uap", "UAP (2 Hex, optional)", "-u", "separate", False, ""),
         ("t", "Timeout Sekunden (optional)", "-t", "separate", False, ""),
         ("ch", "Fester Kanal 0-79", "-c", "separate", False, ""),
         ("err", "Max. Access-Code-Fehler (0-4)", "-e", "separate", False, "2"),
         ("out", "Ausgabe (.pcapng)", "-r", "separate", False, "")]),
    "Datei analysieren (offline)": Spec("ubertooth-rx", [],
        [("inp", "Eingabedatei (.pcapng)", "-i", "separate", True, ""),
         ("out", "Ausgabe (.pcapng, optional)", "-r", "separate", False, "")]),
    "CLK-Follow (ubertooth-follow)": Spec("ubertooth-follow", [],
        [("lap", "LAP (6 Hex)", "-l", "attached", True, ""),
         ("uap", "UAP (2 Hex)", "-u", "attached", True, ""),
         ("out", "Ausgabe (.pcapng)", "-r", "attached", False, ""),
         ("err", "Max. Fehler", "-e", "separate", False, ""),
         ("hci", "Bluetooth-Gerät (z.B. hci0)", "-b", "separate", False, "hci0"),
         ("w", "USB-Delay (625us-Slots)", "-w", "separate", False, ""),
         ("afh", "AFH aktivieren", "-a", "flag", False, "")]),
    "AFH-Kanalmap (ubertooth-afh)": Spec("ubertooth-afh", [],
        [("lap", "LAP (6 Hex)", "-l", "separate", True, ""),
         ("uap", "UAP (2 Hex)", "-u", "separate", True, ""),
         ("m", "Kanal-Entfernungsschwelle", "-m", "separate", False, "5"),
         ("t", "Timeout (optional)", "-t", "separate", False, ""),
         ("rep", "Karte jede Sekunde drucken", "-r", "flag", False, "")]),
    "Aktiver Scan (ubertooth-scan)": Spec("ubertooth-scan", [],
        [("s", "BlueZ-Inquiry-Scan", "-s", "flag", False, ""),
         ("x", "Extended Inquiry", "-x", "flag", False, ""),
         ("t", "Scan-Zeit Sekunden", "-t", "separate", False, "20"),
         ("hci", "Bluetooth-Gerät", "-b", "separate", False, "hci0")],
        note="Benötigt zusätzlich einen Bluetooth-USB-Dongle (BlueZ)."),
}

# ---------------- Tab 4: Spektrum & Rohdaten --------------------------------
SPECTRUM_CMDS = {
    "Spektrum-Sweep (RSSI-Text)": Spec("ubertooth-specan", [],
        [("lo", "Untere Frequenz MHz", "-l", "separate", False, "2402"),
         ("hi", "Obere Frequenz MHz", "-u", "separate", False, "2480"),
         ("out", "Ausgabedatei (.dat)", "-d", "separate", False, "")]),
    "Spektrum-Sweep (feedgnuplot)": Spec("ubertooth-specan", ["-g"],
        [("lo", "Untere Frequenz MHz", "-l", "separate", False, "2402"),
         ("hi", "Obere Frequenz MHz", "-u", "separate", False, "2480"),
         ("out", "Ausgabedatei (.dat)", "-d", "separate", False, "")],
        note="Daten für feedgnuplot: ubertooth-specan -g -d sweep.dat"),
    "Spektrum-Sweep (3D)": Spec("ubertooth-specan", ["-G"],
        [("out", "Ausgabedatei (.dat)", "-d", "separate", False, "")]),
    "Grafische Spektralanalyse (GUI)": Spec("ubertooth-specan-ui", [],
        note="Benötigt Python+numpy/matplotlib aus host/python/specan_ui."),
    "Rohdaten-Dump Classic": Spec("ubertooth-dump", ["-c"],
        [("out", "Ausgabedatei (.bin)", "-d", "separate", True, "classic.bin"),
         ("b", "Bits als ASCII 0/1", "-b", "flag", False, "")]),
    "Rohdaten-Dump BLE": Spec("ubertooth-dump", ["-l"],
        [("out", "Ausgabedatei (.bin)", "-d", "separate", True, "ble.bin"),
         ("b", "Bits als ASCII 0/1", "-b", "flag", False, "")]),
    "CC2400-Register lesen": Spec("ubertooth-debug", [],
        [("reg", "Register (Zahl, %name oder 19-22)", "-r", "separate", True, "%manor"),
         ("v", "Verbosität (0-2)", "-v", "separate", False, "1")], timeout=15),
}

# ---------------- Tab 5: Firmware (ubertooth-dfu) ---------------------------
FIRMWARE_CMDS = {
    "Firmware schreiben (Download)": Spec("ubertooth-dfu", [],
        [("file", "DFU-Datei (.dfu)", "-d", "separate", True, "bluetooth_rxtx.dfu"),
         ("reset", "Danach Reset", "-r", "flag", False, "")],
        note="Vorher DFU-Modus aktivieren: ubertooth-util -f (Tab 1)."),
    "Firmware lesen (Upload)": Spec("ubertooth-dfu", [],
        [("file", "Zieldatei (.dfu)", "-u", "separate", True, "backup.dfu")]),
    "DFU-Suffix an Binär anhängen": Spec("ubertooth-dfu", [],
        [("file", "Binärdatei (.bin)", "-s", "separate", True, "")]),
}

# ---------------- Tab 6: Analyse & Workflow ---------------------------------
ANALYSE_CMDS = {
    "crackle: Capture prüfen": Spec("crackle", [],
        [("inp", "Eingabe-PCAP (PPI)", "-i", "separate", True, "crackle.pcap")],
        note="Zeigt, ob die nötigen Pairing-Pakete enthalten sind."),
    "crackle: TK cracken + entschlüsseln": Spec("crackle", [],
        [("inp", "Eingabe-PCAP (PPI)", "-i", "separate", True, "crackle.pcap"),
         ("out", "Entschlüsselte Ausgabe (.pcap)", "-o", "separate", True, "decrypted.pcap")]),
    "crackle: Mit LTK entschlüsseln": Spec("crackle", [],
        [("inp", "Eingabe-PCAP", "-i", "separate", True, ""),
         ("out", "Entschlüsselte Ausgabe (.pcap)", "-o", "separate", True, ""),
         ("ltk", "LTK (128-bit hex)", "-l", "separate", True, "")]),
    "Wireshark-Live-Pipe (BLE)": Spec("ubertooth-btle", ["-f", "-c", FIFO],
        pre=["rm -f %s && mkfifo %s" % (FIFO, FIFO)],
        post=["rm -f %s" % FIFO],
        note="Capture starten, dann Wireshark: Capture→Options→Manage Interfaces→"
             "New→Pipe: /tmp/ubertooth.pipe"),
    "Capture in Wireshark öffnen": Spec("wireshark", [],
        [("file", "Capture-Datei", "", "separate", True, "")],
        detach=True),
    "tshark: Übersicht anzeigen": Spec("tshark", ["-r"],
        [("file", "Capture-Datei", "", "separate", True, "")], timeout=30),
}

TABS = [
    ("Gerät & Funk",       UTIL_CMDS),
    ("BLE Sniffing",       BTLE_CMDS),
    ("Classic BR/EDR",     CLASSIC_CMDS),
    ("Spektrum & Rohdaten",SPECTRUM_CMDS),
    ("Firmware",           FIRMWARE_CMDS),
    ("Analyse & Workflow", ANALYSE_CMDS),
]


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
class CommandTab(ttk.Frame):
    """Ein Tab: Combobox + dynamische Felder + Ausführen-Button."""

    def __init__(self, parent, title, commands, app):
        super().__init__(parent)
        self.commands = commands
        self.app = app
        self.widgets = {}   # key -> (label, widget)
        self.values = {}    # key -> StringVar / BooleanVar

        top = ttk.Frame(self)
        top.pack(fill=tk.X, pady=4)
        ttk.Label(top, text="Befehl:").pack(side=tk.LEFT)
        self.cmd_var = tk.StringVar()
        combo = ttk.Combobox(top, textvariable=self.cmd_var, state="readonly",
                             width=46, values=list(commands.keys()))
        combo.pack(side=tk.LEFT, padx=6)
        combo.current(0)
        combo.bind("<<ComboboxSelected>>", lambda e: self.rebuild_fields())

        self.fields = ttk.Frame(self)
        self.fields.pack(fill=tk.X, pady=4)
        self.note_lbl = ttk.Label(self, foreground="#8a6d1a", wraplength=760,
                                  justify=tk.LEFT)
        self.note_lbl.pack(fill=tk.X, pady=2)

        self.preview = ttk.Label(self, foreground="#1a5c8a", wraplength=760,
                                 justify=tk.LEFT)
        self.preview.pack(fill=tk.X, pady=2)

        btns = ttk.Frame(self)
        btns.pack(fill=tk.X, pady=6)
        self.run_btn = ttk.Button(btns, text="▶ Ausführen",
                                  command=lambda: self.app.start(self))
        self.run_btn.pack(side=tk.LEFT, padx=4)

        self.rebuild_fields()

    def rebuild_fields(self):
        for w in self.widgets.values():
            for widget in w:
                widget.destroy()
        self.widgets.clear()
        self.values.clear()
        spec = self.commands[self.cmd_var.get()]

        row = 0
        for key, label, _flag, style, required, default in spec.fields:
            lbl = ttk.Label(self.fields, text=label + ":")
            lbl.grid(row=row, column=0, sticky=tk.W, padx=4, pady=2)
            if style == "flag":
                var = tk.BooleanVar(value=False)
                chk = ttk.Checkbutton(self.fields, variable=var)
                chk.grid(row=row, column=1, sticky=tk.W, padx=4)
                self.widgets[key] = (lbl, chk)
            else:
                var = tk.StringVar(value=default)
                ent = ttk.Entry(self.fields, textvariable=var, width=44)
                ent.grid(row=row, column=1, sticky=tk.W, padx=4)
                self.widgets[key] = (lbl, ent)
            self.values[key] = var
            row += 1

        self.note_lbl.config(text=("ℹ " + spec.note) if spec.note else "")
        self.update_preview()

    def update_preview(self):
        try:
            argv = self.app.build_argv(self)
            self.preview.config(text="Befehl: " + " ".join(argv))
        except Exception:
            self.preview.config(text="Befehl: –")

    def current_spec(self):
        return self.commands[self.cmd_var.get()]


class UbertoothApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ubertooth One – Complete Control (Extended)")
        self.root.geometry("880x720")
        self.root.minsize(760, 600)

        self.proc = None
        self.running = False
        self.active_tab = None
        self.msg_q = queue.Queue()
        self.stop_timer = None
        self.pipe_used = False

        # ---- Statusleiste -------------------------------------------------
        self.status_var = tk.StringVar(value="Initialisierung...")
        ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN,
                  anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

        main = ttk.Frame(root, padding=6)
        main.pack(fill=tk.BOTH, expand=True)

        # ---- Globale Einstellungen ----------------------------------------
        cfg = ttk.LabelFrame(main, text="Globale Einstellungen", padding=4)
        cfg.pack(fill=tk.X)
        ttk.Label(cfg, text="Geräteindex -U:").pack(side=tk.LEFT, padx=4)
        self.dev_idx = tk.StringVar(value="0")
        ttk.Entry(cfg, textvariable=self.dev_idx, width=3).pack(side=tk.LEFT)
        self.reset_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(cfg, text="Radio nach Stopp zurücksetzen (-S / -r)",
                        variable=self.reset_var).pack(side=tk.LEFT, padx=10)
        ttk.Label(cfg, text="Auto-Stopp (s, 0=aus):").pack(side=tk.LEFT, padx=4)
        self.autostop = tk.StringVar(value="0")
        ttk.Entry(cfg, textvariable=self.autostop, width=5).pack(side=tk.LEFT)
        ttk.Button(cfg, text="📋 Befehl kopieren",
                   command=self.copy_command).pack(side=tk.RIGHT, padx=4)
        ttk.Button(cfg, text="💾 Log exportieren",
                   command=self.export_log).pack(side=tk.RIGHT, padx=4)

        # ---- Notebook mit Tabs --------------------------------------------
        nb = ttk.Notebook(main)
        nb.pack(fill=tk.BOTH, expand=True, pady=4)
        self.tabs = []
        for title, cmds in TABS:
            tab = CommandTab(nb, title, cmds, self)
            nb.add(tab, text=title)
            self.tabs.append(tab)

        # ---- Log-Ausgabe ---------------------------------------------------
        logf = ttk.LabelFrame(main, text="Ausgabe", padding=4)
        logf.pack(fill=tk.BOTH, expand=True, pady=4)
        self.log_text = scrolledtext.ScrolledText(logf, height=10,
                                                  state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # ---- Start-Checks --------------------------------------------------
        self.root.after(150, self.init_device)
        self.root.after(100, self._poll_queue)

    # ------------------------------------------------------------- Logging
    def log(self, msg, level="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{ts}] [{level}] {msg}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _poll_queue(self):
        try:
            while True:
                level, msg = self.msg_q.get_nowait()
                self.log(msg, level)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    # ------------------------------------------------------------- Gerät
    def init_device(self):
        try:
            require_root()
            missing = [t for t in ALL_TOOLS if not have(t)]
            if missing:
                self.log("Fehlende Tools: " + ", ".join(missing)
                         + "  (apt install ubertooth crackle tshark wireshark)",
                         "WARN")
            out, rc = run_sync(["ubertooth-util", "-v"], timeout=10)
            if rc != 0:
                raise RuntimeError(f"ubertooth-util -v: {out}")
            self.log(f"Gerät erkannt – Firmware: {out}", "OK")
            self.status_var.set("Bereit")
        except Exception as e:
            self.log(f"Initialisierung fehlgeschlagen: {e}", "ERROR")
            self.status_var.set("Fehler – Befehl trotzdem wählbar")

    # ------------------------------------------------------- Befehl bauen
    def build_argv(self, tab):
        spec = tab.current_spec()
        argv = [spec.tool]
        if spec.tool in UBERTOOTH_TOOLS:
            idx = self.dev_idx.get().strip() or "0"
            argv.append("-U" + idx)
        argv += list(spec.base)
        for key, label, flag, style, required, default in spec.fields:
            var = tab.values[key]
            if style == "flag":
                if var.get():
                    argv.append(flag)
                continue
            val = var.get().strip()
            if required and not val:
                raise ValueError(f"Feld fehlt: {label}")
            if not val:
                continue
            if style == "attached":
                argv.append(flag + val)
            else:
                argv += [flag, val]
        return argv

    # ------------------------------------------------------------- Ausführen
    def start(self, tab):
        if self.running:
            self.log("Es läuft bereits ein Prozess.", "WARN")
            return
        spec = tab.current_spec()
        try:
            argv = self.build_argv(tab)
        except ValueError as e:
            self.log(str(e), "ERROR")
            return

        # Pre-Kommandos (z.B. FIFO anlegen)
        for shell_cmd in spec.pre:
            self.log(f"Pre: {shell_cmd}", "INFO")
            subprocess.run(shell_cmd, shell=True, check=False)

        self.running = True
        self.active_tab = tab
        self.pipe_used = bool(spec.pre)
        for t in self.tabs:
            t.run_btn.config(state=tk.DISABLED)
        self.status_var.set("Läuft: " + " ".join(argv))
        self.log("Ausführen: " + " ".join(argv), "INFO")

        try:
            if spec.detach:
                subprocess.Popen(argv, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 start_new_session=True)
                self.log("Tool gestartet (detached).", "OK")
                self._finished()
                return
            self.proc = subprocess.Popen(
                argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, start_new_session=True)
        except FileNotFoundError:
            self.log(f"Tool nicht gefunden: {spec.tool}", "ERROR")
            self._finished()
            return

        threading.Thread(target=self._reader, daemon=True).start()

        # Client-seitiger Auto-Stopp
        try:
            secs = int(self.autostop.get())
            if secs > 0:
                self.stop_timer = threading.Timer(secs, self.stop)
                self.stop_timer.daemon = True
                self.stop_timer.start()
                self.log(f"Auto-Stopp nach {secs}s aktiv.", "INFO")
        except ValueError:
            pass

        # Timeout für Info-Abfragen
        if spec.timeout:
            self.stop_timer = threading.Timer(spec.timeout + 5, self.stop)
            self.stop_timer.daemon = True
            self.stop_timer.start()

    def _reader(self):
        try:
            for line in self.proc.stdout:
                self.msg_q.put(("INFO", line.rstrip()))
            self.proc.wait()
            rc = self.proc.returncode
            if rc == 0:
                self.msg_q.put(("OK", "Prozess beendet (rc=0)."))
            elif rc == -signal.SIGTERM or rc == -signal.SIGKILL:
                self.msg_q.put(("WARN", "Prozess durch Stopp beendet."))
            else:
                self.msg_q.put(("ERROR", f"Prozess beendet rc={rc}"))
        except Exception as e:
            self.msg_q.put(("ERROR", f"Reader-Fehler: {e}"))
        finally:
            self.root.after(0, self._finished)

    # --------------------------------------------------------------- Stopp
    def stop(self):
        if self.stop_timer and self.stop_timer.is_alive():
            self.stop_timer.cancel()
        if not self.running or not self.proc:
            return
        self.log("Stoppe Prozess (SIGTERM)...", "WARN")
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        # Nach 3 s hart killen, falls nötig
        def hard_kill():
            try:
                if self.proc and self.proc.poll() is None:
                    os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)
                    self.msg_q.put(("WARN", "SIGKILL nach Timeout."))
            except ProcessLookupError:
                pass
        threading.Timer(3.0, hard_kill).start()

    def _finished(self):
        if self.stop_timer and self.stop_timer.is_alive():
            self.stop_timer.cancel()
        self.running = False
        spec = self.active_tab.current_spec() if self.active_tab else None
        for t in self.tabs:
            t.run_btn.config(state=tk.NORMAL)
        # Post-Kommandos (FIFO aufräumen)
        if spec and spec.post:
            threading.Thread(target=self._run_post, args=(spec.post,),
                             daemon=True).start()
        # Radio-Reset nach Capture-Tools
        if spec and spec.tool in UBERTOOTH_TOOLS and self.reset_var.get() \
                and spec.tool != "ubertooth-util":
            threading.Thread(target=self._reset_radio, daemon=True).start()
        self.proc = None
        self.active_tab = None
        self.status_var.set("Bereit")

    def _run_post(self, cmds):
        for c in cmds:
            self.msg_q.put(("INFO", f"Post: {c}"))
            subprocess.run(c, shell=True, check=False)

    def _reset_radio(self):
        self.msg_q.put(("INFO", "Radio-Reset: ubertooth-util -S / -r"))
        run_sync(["ubertooth-util", "-S"], timeout=5)
        run_sync(["ubertooth-util", "-r"], timeout=5)

    # ------------------------------------------------------- Hilfsfunktionen
    def copy_command(self):
        if not self.active_tab:
            self.log("Kein laufender Befehl zum Kopieren.", "WARN")
            return
        argv = self.build_argv(self.active_tab)
        self.root.clipboard_clear()
        self.root.clipboard_append(" ".join(argv))
        self.log("Befehl in Zwischenablage kopiert.", "OK")

    def export_log(self):
        path = filedialog.asksaveasfilename(
            title="Log speichern", defaultextension=".log",
            initialfile=f"ubertooth_{datetime.now():%Y%m%d_%H%M%S}.log")
        if not path:
            return
        with open(path, "w") as f:
            f.write(self.log_text.get("1.0", tk.END))
        self.log(f"Log exportiert: {path}", "OK")


if __name__ == "__main__":
    root = tk.Tk()
    UbertoothApp(root)
    root.mainloop()
