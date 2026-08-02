#!/usr/bin/env python3
"""
Ubertooth One – Complete Control GUI (i18n Edition)
====================================================
Vollständige grafische Oberfläche für ALLE echten Ubertooth-Tools
(verifiziert gegen die Manpages von Ubuntu/Kali und die Doku von
greatscottgadgets/ubertooth).

SPRACHEN:
  - Eingebaute Sprachen: Deutsch (Standard), Englisch
  - Beliebig viele weitere Sprachen per JSON-Sprachpaket:
      * Ordner "langs/" neben dem Skript wird beim Start automatisch geladen
      * Oder: "Pack laden…"-Button (Dateidialog)
  - Sprachumschaltung live, ohne Neustart
  - Fehlende Schlüssel fallen auf Englisch zurück (Fallback)
  - "Template"-Button exportiert eine leere Übersetzungsvorlage (.json)

TOOLS:
  ubertooth-util / ubertooth-btle / ubertooth-rx / ubertooth-follow /
  ubertooth-afh / ubertooth-scan / ubertooth-specan / ubertooth-specan-ui /
  ubertooth-dump / ubertooth-debug / ubertooth-dfu / crackle / tshark / wireshark

Erfordert Root und mindestens einen angeschlossenen Ubertooth One/Zero.
"""
import json
import os
import queue
import signal
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime

# ===========================================================================
# 1) I18N – Übersetzungssystem
# ===========================================================================
class Translator:
    def __init__(self):
        self.packs = {}                 # code -> {"name": str, "strings": dict}
        self.current = "de"             # Startsprache
        self._builtin = {"en", "de"}
        self._register_builtin_en()
        self._register_builtin_de()

    # ------------------------------------------------------------- Registrierung
    def _register(self, code, name, strings):
        self.packs[code] = {"name": name, "strings": strings}

    def _register_builtin_en(self):
        self._register("en", "English", {
            "app.title": "Ubertooth One – Complete Control",

            "ui.settings": "Settings",
            "ui.language": "Language:",
            "ui.load_pack": "Load pack…",
            "ui.export_template": "Template",
            "ui.device_index": "Device index -U:",
            "ui.reset_radio": "Reset radio after stop (-S / -r)",
            "ui.auto_stop": "Auto-stop (s, 0=off):",
            "ui.copy": "Copy command",
            "ui.export_log": "Export log",
            "ui.stop": "■ Stop",
            "ui.output": "Output",
            "ui.command": "Command:",
            "ui.execute": "▶ Execute",
            "ui.preview": "Command:",
            "ui.status_ready": "Ready",
            "ui.status_error": "Error",
            "ui.status_init": "Initializing…",
            "ui.status_running": "Running: {cmd}",

            "tab.device": "Device & Radio",
            "tab.ble": "BLE Sniffing",
            "tab.classic": "Classic BR/EDR",
            "tab.spectrum": "Spectrum & Raw Data",
            "tab.firmware": "Firmware",
            "tab.analyze": "Analysis & Workflow",

            "log.missing_tools": "Missing tools: {tools} (apt install ubertooth crackle tshark wireshark)",
            "log.device_ok": "Device detected – firmware: {fw}",
            "log.init_failed": "Initialization failed: {err}",
            "log.pre": "Pre: {cmd}",
            "log.executing": "Executing: {cmd}",
            "log.detached": "Tool started (detached).",
            "log.tool_missing": "Tool not found: {tool}",
            "log.auto_stop": "Auto-stop armed for {secs}s.",
            "log.finished_ok": "Process finished (rc=0).",
            "log.stopped_sig": "Process terminated by stop.",
            "log.failed_rc": "Process exited rc={rc}",
            "log.reader_error": "Reader error: {err}",
            "log.stop_sigterm": "Stopping process (SIGTERM)…",
            "log.stop_sigkill": "SIGKILL after timeout.",
            "log.reset_radio": "Radio reset: ubertooth-util -S / -r",
            "log.post": "Post: {cmd}",
            "log.copied": "Command copied to clipboard.",
            "log.no_running": "No running command to copy.",
            "log.exported": "Log exported: {path}",
            "log.running_blocked": "A process is already running.",
            "log.field_missing": "Field required: {label}",
            "log.pack_loaded": "Loaded language pack: {name}",
            "log.pack_invalid": "Invalid language pack: {err}",
            "log.lang_changed": "Language switched to: {name}",
            "log.missing_keys": "Note: {n} keys missing in this language (fallback: English).",

            # Befehlsnamen – Gerät & Funk
            "util.identify": "Identify (blink LEDs)",
            "util.fw_rev": "Firmware revision",
            "util.compile": "Compile info",
            "util.board": "Board ID",
            "util.part": "Part ID (MCU)",
            "util.serial": "Serial number",
            "util.count": "Number of attached devices",
            "util.reset": "Full reset",
            "util.stop": "Stop operation",
            "util.dfu": "Enter DFU mode (firmware)",
            "util.isp": "Enter ISP mode",
            "util.pa": "Set PA level",
            "util.chan_mhz": "Set channel (MHz)",
            "util.chan_idx": "Set channel (index)",
            "util.squelch": "Set squelch",
            "util.led_spectrum": "LED spectrum analyzer",
            "util.leds": "Set all LEDs",
            "util.usr_led": "Set USR LED",
            "util.tx_test": "Transmit test (continuous)",
            "util.repeater": "Repeater mode",
            "util.rng_start": "Start range test",
            "util.rng_result": "Range test result",
            "util.xmas": "Xmas lights (LED show)",

            # Befehlsnamen – BLE
            "btle.follow": "Follow capture (PCAPNG)",
            "btle.follow_target": "Follow capture (targeted)",
            "btle.promisc": "Promiscuous capture",
            "btle.adv": "Advertising scan (adv. only)",
            "btle.faux": "Faux-slave (inject advertising)",
            "btle.interfere": "Interfere with connection",
            "btle.crc": "Set CRC verification",
            "btle.set_aa": "Set access address",
            "btle.crackle_cap": "Capture for crackle (PPI-PCAP)",
            "btle.le_pcap": "Capture as PCAP (LE pseudoheader)",

            # Befehlsnamen – Classic
            "classic.survey": "Survey mode (all piconets)",
            "classic.follow": "Follow piconet (LAP/UAP)",
            "classic.offline": "Analyze file (offline)",
            "classic.clk_follow": "CLK follow (ubertooth-follow)",
            "classic.afh": "AFH channel map (ubertooth-afh)",
            "classic.scan": "Active scan (ubertooth-scan)",

            # Befehlsnamen – Spektrum & Rohdaten
            "spec.sweep": "Spectrum sweep (RSSI text)",
            "spec.feed": "Spectrum sweep (feedgnuplot)",
            "spec.feed3d": "Spectrum sweep (3D)",
            "spec.gui": "Graphical spectrum analyzer",
            "spec.dump_c": "Raw bitstream dump Classic",
            "spec.dump_l": "Raw bitstream dump BLE",
            "spec.debug": "Read CC2400 registers",

            # Befehlsnamen – Firmware
            "fw.write": "Write firmware (download)",
            "fw.read": "Read firmware (upload)",
            "fw.suffix": "Add DFU suffix to binary",

            # Befehlsnamen – Analyse
            "an.crackle_check": "crackle: inspect capture",
            "an.crackle_crack": "crackle: crack TK + decrypt",
            "an.crackle_ltk": "crackle: decrypt with LTK",
            "an.pipe": "Wireshark live pipe (BLE)",
            "an.open": "Open capture in Wireshark",
            "an.tshark": "tshark: show overview",

            # Feld-Labels
            "fld.pa": "PA level (0-7)",
            "fld.chmhz": "Channel MHz (2400-2483)",
            "fld.chidx": "Channel index (0-78)",
            "fld.sql": "Squelch dBm (e.g. -50)",
            "fld.rssi": "RSSI threshold (1-225)",
            "fld.leds": "All LEDs (0/1)",
            "fld.usr": "USR LED (0/1)",
            "fld.out": "Output file (.pcapng)",
            "fld.target": "Target BD_ADDR",
            "fld.advch": "Adv channel 37/38/39",
            "fld.aa": "Access address (hex)",
            "fld.bdaddr": "Own BD_ADDR",
            "fld.crc": "CRC mode (0/1)",
            "fld.out_pcap": "Output file (.pcap)",
            "fld.t_secs": "Timeout seconds",
            "fld.out_opt": "Output file (optional)",
            "fld.lap": "LAP (6 hex)",
            "fld.uap": "UAP (2 hex)",
            "fld.ch": "Fixed channel 0-79",
            "fld.err": "Max access code errors (0-4)",
            "fld.inp": "Input file (.pcapng)",
            "fld.hci": "Bluetooth device (hci0)",
            "fld.w": "USB delay (625us slots)",
            "fld.m": "Channel removal threshold",
            "fld.t_opt": "Timeout (optional)",
            "fld.lo": "Lower frequency MHz",
            "fld.hi": "Upper frequency MHz",
            "fld.out_dat": "Output file (.dat)",
            "fld.reg": "Register (num, %name, 19-22)",
            "fld.verb": "Verbosity (0-2)",
            "fld.dfu_file": "DFU file (.dfu)",
            "fld.dfu_out": "Target file (.dfu)",
            "fld.bin_file": "Binary file (.bin)",
            "fld.pcap_in": "Input PCAP (PPI)",
            "fld.pcap_out": "Decrypted output (.pcap)",
            "fld.ltk": "LTK (128-bit hex)",
            "fld.file": "Capture file",

            # Checkboxen
            "chk.bits": "Print bits as ASCII 0/1",
            "chk.inquiry": "BlueZ inquiry scan",
            "chk.extended": "Extended inquiry",
            "chk.repeat": "Print map every second",
            "chk.afh": "Enable AFH",
            "chk.reset": "Reset afterwards",

            # Hinweise
            "note.led_spec": "Runs until stopped. Evaluation via ubertooth-specan.",
            "note.tx": "TRANSMITS! Check radio regulations (FTEG/EMVG).",
            "note.faux": "Injects advertising packets with own MAC – TRANSMITS!",
            "note.interfere": "Interferes with connections – only with permission!",
            "note.crackle": "PPI format – input for crackle.",
            "note.scan": "Requires an additional Bluetooth USB dongle (BlueZ).",
            "note.feed": "Data for feedgnuplot: ubertooth-specan -g -d sweep.dat",
            "note.specan_ui": "Needs Python+numpy/matplotlib from host/python/specan_ui.",
            "note.dfu": "Activate DFU mode first: ubertooth-util -f (Device tab).",
            "note.crackle_check": "Shows whether the required pairing packets are present.",
            "note.pipe": "Start capture, then Wireshark: Capture→Options→Manage Interfaces→New→Pipe: /tmp/ubertooth.pipe",
        })

    def _register_builtin_de(self):
        self._register("de", "Deutsch", {
            "app.title": "Ubertooth One – Complete Control",

            "ui.settings": "Einstellungen",
            "ui.language": "Sprache:",
            "ui.load_pack": "Pack laden…",
            "ui.export_template": "Vorlage",
            "ui.device_index": "Geräteindex -U:",
            "ui.reset_radio": "Radio nach Stopp zurücksetzen (-S / -r)",
            "ui.auto_stop": "Auto-Stopp (s, 0=aus):",
            "ui.copy": "Befehl kopieren",
            "ui.export_log": "Log exportieren",
            "ui.stop": "■ Stopp",
            "ui.output": "Ausgabe",
            "ui.command": "Befehl:",
            "ui.execute": "▶ Ausführen",
            "ui.preview": "Befehl:",
            "ui.status_ready": "Bereit",
            "ui.status_error": "Fehler",
            "ui.status_init": "Initialisierung…",
            "ui.status_running": "Läuft: {cmd}",

            "tab.device": "Gerät & Funk",
            "tab.ble": "BLE Sniffing",
            "tab.classic": "Classic BR/EDR",
            "tab.spectrum": "Spektrum & Rohdaten",
            "tab.firmware": "Firmware",
            "tab.analyze": "Analyse & Workflow",

            "log.missing_tools": "Fehlende Tools: {tools} (apt install ubertooth crackle tshark wireshark)",
            "log.device_ok": "Gerät erkannt – Firmware: {fw}",
            "log.init_failed": "Initialisierung fehlgeschlagen: {err}",
            "log.pre": "Pre: {cmd}",
            "log.executing": "Ausführen: {cmd}",
            "log.detached": "Tool gestartet (detached).",
            "log.tool_missing": "Tool nicht gefunden: {tool}",
            "log.auto_stop": "Auto-Stopp nach {secs}s aktiv.",
            "log.finished_ok": "Prozess beendet (rc=0).",
            "log.stopped_sig": "Prozess durch Stopp beendet.",
            "log.failed_rc": "Prozess beendet rc={rc}",
            "log.reader_error": "Reader-Fehler: {err}",
            "log.stop_sigterm": "Stoppe Prozess (SIGTERM)…",
            "log.stop_sigkill": "SIGKILL nach Timeout.",
            "log.reset_radio": "Radio-Reset: ubertooth-util -S / -r",
            "log.post": "Post: {cmd}",
            "log.copied": "Befehl in Zwischenablage kopiert.",
            "log.no_running": "Kein laufender Befehl zum Kopieren.",
            "log.exported": "Log exportiert: {path}",
            "log.running_blocked": "Es läuft bereits ein Prozess.",
            "log.field_missing": "Feld fehlt: {label}",
            "log.pack_loaded": "Sprachpaket geladen: {name}",
            "log.pack_invalid": "Ungültiges Sprachpaket: {err}",
            "log.lang_changed": "Sprache gewechselt zu: {name}",
            "log.missing_keys": "Hinweis: {n} Schlüssel fehlen in dieser Sprache (Fallback: Englisch).",

            "util.identify": "Identifikation (LEDs blinken)",
            "util.fw_rev": "Firmware-Revision",
            "util.compile": "Kompilier-Info",
            "util.board": "Board-ID",
            "util.part": "Part ID (Mikrocontroller)",
            "util.serial": "Seriennummer",
            "util.count": "Anzahl angeschlossener Geräte",
            "util.reset": "Voll-Reset",
            "util.stop": "Operation stoppen",
            "util.dfu": "DFU-Modus aktivieren (Firmware)",
            "util.isp": "ISP-Modus aktivieren",
            "util.pa": "PA-Level setzen",
            "util.chan_mhz": "Kanal setzen (MHz)",
            "util.chan_idx": "Kanal setzen (Index)",
            "util.squelch": "Squelch setzen",
            "util.led_spectrum": "LED-Spektrumanalyzer",
            "util.leds": "Alle LEDs setzen",
            "util.usr_led": "USR-LED setzen",
            "util.tx_test": "Transmittest (Dauer-Senden)",
            "util.repeater": "Repeater-Modus",
            "util.rng_start": "Reichweitentest starten",
            "util.rng_result": "Reichweitentest Ergebnis",
            "util.xmas": "Xmas-Lights (LED-Show)",

            "btle.follow": "Follow-Capture (PCAPNG)",
            "btle.follow_target": "Follow-Capture gezielt",
            "btle.promisc": "Promiscuous-Capture",
            "btle.adv": "Advertising-Scan (nur Werbung)",
            "btle.faux": "Faux-Slave (Advertising injizieren)",
            "btle.interfere": "Interferenz auf Verbindung",
            "btle.crc": "CRC-Verifikation setzen",
            "btle.set_aa": "Access-Address setzen",
            "btle.crackle_cap": "Capture für crackle (PPI-PCAP)",
            "btle.le_pcap": "Capture als PCAP (LE-Pseudoheader)",

            "classic.survey": "Survey-Modus (alle Piconets)",
            "classic.follow": "Piconet folgen (LAP/UAP)",
            "classic.offline": "Datei analysieren (offline)",
            "classic.clk_follow": "CLK-Follow (ubertooth-follow)",
            "classic.afh": "AFH-Kanalmap (ubertooth-afh)",
            "classic.scan": "Aktiver Scan (ubertooth-scan)",

            "spec.sweep": "Spektrum-Sweep (RSSI-Text)",
            "spec.feed": "Spektrum-Sweep (feedgnuplot)",
            "spec.feed3d": "Spektrum-Sweep (3D)",
            "spec.gui": "Grafische Spektralanalyse (GUI)",
            "spec.dump_c": "Rohdaten-Dump Classic",
            "spec.dump_l": "Rohdaten-Dump BLE",
            "spec.debug": "CC2400-Register lesen",

            "fw.write": "Firmware schreiben (Download)",
            "fw.read": "Firmware lesen (Upload)",
            "fw.suffix": "DFU-Suffix an Binär anhängen",

            "an.crackle_check": "crackle: Capture prüfen",
            "an.crackle_crack": "crackle: TK cracken + entschlüsseln",
            "an.crackle_ltk": "crackle: Mit LTK entschlüsseln",
            "an.pipe": "Wireshark-Live-Pipe (BLE)",
            "an.open": "Capture in Wireshark öffnen",
            "an.tshark": "tshark: Übersicht anzeigen",

            "fld.pa": "PA-Level (0-7)",
            "fld.chmhz": "Kanal MHz (2400-2483)",
            "fld.chidx": "Kanal-Index (0-78)",
            "fld.sql": "Squelch dBm (z.B. -50)",
            "fld.rssi": "RSSI-Schwelle (1-225)",
            "fld.leds": "Alle LEDs (0=aus/1=an)",
            "fld.usr": "USR-LED (0=aus/1=an)",
            "fld.out": "Ausgabedatei (.pcapng)",
            "fld.target": "Ziel-BD_ADDR",
            "fld.advch": "Adv-Kanal 37/38/39",
            "fld.aa": "Access-Address (hex)",
            "fld.bdaddr": "Eigene BD_ADDR",
            "fld.crc": "CRC-Modus (0=aus/1=ein)",
            "fld.out_pcap": "Ausgabedatei (.pcap)",
            "fld.t_secs": "Timeout Sekunden",
            "fld.out_opt": "Ausgabedatei (optional)",
            "fld.lap": "LAP (6 Hex)",
            "fld.uap": "UAP (2 Hex)",
            "fld.ch": "Fester Kanal 0-79",
            "fld.err": "Max. Access-Code-Fehler (0-4)",
            "fld.inp": "Eingabedatei (.pcapng)",
            "fld.hci": "Bluetooth-Gerät (hci0)",
            "fld.w": "USB-Delay (625us-Slots)",
            "fld.m": "Kanal-Entfernungsschwelle",
            "fld.t_opt": "Timeout (optional)",
            "fld.lo": "Untere Frequenz MHz",
            "fld.hi": "Obere Frequenz MHz",
            "fld.out_dat": "Ausgabedatei (.dat)",
            "fld.reg": "Register (Zahl, %name, 19-22)",
            "fld.verb": "Verbosität (0-2)",
            "fld.dfu_file": "DFU-Datei (.dfu)",
            "fld.dfu_out": "Zieldatei (.dfu)",
            "fld.bin_file": "Binärdatei (.bin)",
            "fld.pcap_in": "Eingabe-PCAP (PPI)",
            "fld.pcap_out": "Entschlüsselte Ausgabe (.pcap)",
            "fld.ltk": "LTK (128-bit hex)",
            "fld.file": "Capture-Datei",

            "chk.bits": "Bits als ASCII 0/1",
            "chk.inquiry": "BlueZ-Inquiry-Scan",
            "chk.extended": "Extended Inquiry",
            "chk.repeat": "Karte jede Sekunde drucken",
            "chk.afh": "AFH aktivieren",
            "chk.reset": "Danach Reset",

            "note.led_spec": "Läuft bis zum Stopp. Auswertung über ubertooth-specan.",
            "note.tx": "SENDEN! Rechtslage prüfen (FTEG/EMVG).",
            "note.faux": "Injiziert Advertising-Pakete mit eigener MAC – SENDEN!",
            "note.interfere": "Stört Verbindungen – nur mit Genehmigung!",
            "note.crackle": "PPI-Format – Eingabe für crackle.",
            "note.scan": "Benötigt zusätzlich einen Bluetooth-USB-Dongle (BlueZ).",
            "note.feed": "Daten für feedgnuplot: ubertooth-specan -g -d sweep.dat",
            "note.specan_ui": "Benötigt Python+numpy/matplotlib aus host/python/specan_ui.",
            "note.dfu": "Vorher DFU-Modus aktivieren: ubertooth-util -f (Tab Gerät).",
            "note.crackle_check": "Zeigt, ob die nötigen Pairing-Pakete enthalten sind.",
            "note.pipe": "Capture starten, dann Wireshark: Capture→Options→Manage Interfaces→New→Pipe: /tmp/ubertooth.pipe",
        })

    # --------------------------------------------------------------- Zugriff
    def tr(self, key):
        """Aktuelle Sprache -> Englisch (Fallback) -> Schlüsselname."""
        p = self.packs.get(self.current)
        if p and key in p["strings"]:
            return p["strings"][key]
        en = self.packs.get("en", {}).get("strings", {})
        return en.get(key, key)

    def missing_count(self, code=None):
        code = code or self.current
        s = self.packs.get(code, {}).get("strings", {})
        en = self.packs["en"]["strings"]
        return sum(1 for k in en if k not in s)

    def available(self):
        return sorted(self.packs.items())

    # ------------------------------------------------------------- Laden/Export
    def load_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        meta = data.get("meta", {})
        code = str(data.get("code") or meta.get("code")
                   or os.path.splitext(os.path.basename(path))[0])
        name = str(data.get("name") or meta.get("name") or code)
        strings = data.get("strings")
        if not isinstance(strings, dict):
            raise ValueError("missing 'strings' object")
        if code in self._builtin:
            raise ValueError(f"'{code}' is a built-in language code")
        self.packs[code] = {"name": name,
                            "strings": {str(k): str(v) for k, v in strings.items()}}
        return code

    def load_dir(self, d):
        loaded = []
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".json"):
                    try:
                        loaded.append(self.load_file(os.path.join(d, fn)))
                    except Exception:
                        pass
        return loaded

    def export_template(self, path):
        data = {"meta": {"name": "New language", "code": "xx"},
                "strings": dict(self.packs["en"]["strings"])}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


TR = Translator()


def tr(key):
    return TR.tr(key)


# ===========================================================================
# 2) Konstanten & Befehlsspezifikationen
# ===========================================================================
UBERTOOTH_TOOLS = {
    "ubertooth-util", "ubertooth-btle", "ubertooth-rx", "ubertooth-follow",
    "ubertooth-afh", "ubertooth-scan", "ubertooth-specan", "ubertooth-specan-ui",
    "ubertooth-dump", "ubertooth-debug", "ubertooth-dfu",
}
ALL_TOOLS = sorted(UBERTOOTH_TOOLS | {"crackle", "wireshark", "tshark"})

FIFO = "/tmp/ubertooth.pipe"


def require_root():
    if os.geteuid() != 0:
        raise RuntimeError(tr("log.root_required") if "log.root_required" in
                           TR.packs["en"]["strings"] else "Root privileges required")


def have(tool):
    return subprocess.run(["which", tool], capture_output=True).returncode == 0


def run_sync(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (r.stderr.strip() if r.returncode != 0 else r.stdout.strip(),
                r.returncode)
    except subprocess.TimeoutExpired:
        return ("Timeout", -1)
    except Exception as e:
        return (str(e), -2)


class Spec:
    """(tool, base-Flags, Felder, Timeout, detach, pre, post, note_key)."""
    def __init__(self, tool, base=(), fields=(), timeout=None, detach=False,
                 pre=(), post=(), note_key=""):
        self.tool = tool
        self.base = list(base)
        self.fields = fields      # (key, label_key, flag, style, required, default)
        self.timeout = timeout
        self.detach = detach
        self.pre = list(pre)
        self.post = list(post)
        self.note_key = note_key


# Feld-Abkürzungen (lesbarer Code)
def F_att(key, label, flag, req=True, default=""):
    return (key, label, flag, "attached", req, default)


def F_sep(key, label, flag, req=True, default=""):
    return (key, label, flag, "separate", req, default)


def F_flag(key, label, flag):
    return (key, label, flag, "flag", False, False)


# ---------------- Tab 1: Gerät & Funk -------------------------------------
UTIL_CMDS = {
    "util.identify": Spec("ubertooth-util", ["-I"], timeout=15),
    "util.fw_rev":   Spec("ubertooth-util", ["-v"], timeout=15),
    "util.compile":  Spec("ubertooth-util", ["-V"], timeout=15),
    "util.board":    Spec("ubertooth-util", ["-b"], timeout=15),
    "util.part":     Spec("ubertooth-util", ["-p"], timeout=15),
    "util.serial":   Spec("ubertooth-util", ["-s"], timeout=15),
    "util.count":    Spec("ubertooth-util", ["-N"], timeout=15),
    "util.reset":    Spec("ubertooth-util", ["-r"], timeout=15),
    "util.stop":     Spec("ubertooth-util", ["-S"], timeout=15),
    "util.dfu":      Spec("ubertooth-util", ["-f"], timeout=15),
    "util.isp":      Spec("ubertooth-util", ["-i"], timeout=15),
    "util.pa":       Spec("ubertooth-util", [], [F_att("fld.pa", "fld.pa", "-a")], timeout=15),
    "util.chan_mhz": Spec("ubertooth-util", [], [F_att("fld.chmhz", "fld.chmhz", "-c")], timeout=15),
    "util.chan_idx": Spec("ubertooth-util", [], [F_att("fld.chidx", "fld.chidx", "-C")], timeout=15),
    "util.squelch":  Spec("ubertooth-util", [], [F_att("fld.sql", "fld.sql", "-z")], timeout=15),
    "util.led_spectrum": Spec("ubertooth-util", [],
                              [F_att("fld.rssi", "fld.rssi", "-q")],
                              note_key="note.led_spec"),
    "util.leds":     Spec("ubertooth-util", [], [F_att("fld.leds", "fld.leds", "-d")], timeout=15),
    "util.usr_led":  Spec("ubertooth-util", [], [F_att("fld.usr", "fld.usr", "-l")], timeout=15),
    "util.tx_test":  Spec("ubertooth-util", ["-t"], note_key="note.tx"),
    "util.repeater": Spec("ubertooth-util", ["-e"], timeout=15),
    "util.rng_start":   Spec("ubertooth-util", ["-n"], timeout=15),
    "util.rng_result":  Spec("ubertooth-util", ["-m"], timeout=15),
    "util.xmas":     Spec("ubertooth-util", ["-x"], timeout=15),
}

# ---------------- Tab 2: BLE ----------------------------------------------
BTLE_CMDS = {
    "btle.follow": Spec("ubertooth-btle", ["-f"],
        [F_att("fld.out", "fld.out", "-r", True, "capture.pcapng"),
         F_att("fld.target", "fld.target", "-t", False, ""),
         F_att("fld.advch", "fld.advch", "-A", False, "37")]),
    "btle.follow_target": Spec("ubertooth-btle", ["-f"],
        [F_att("fld.target", "fld.target", "-t"),
         F_att("fld.out", "fld.out", "-r", False, "")]),
    "btle.promisc": Spec("ubertooth-btle", ["-p"],
        [F_att("fld.out", "fld.out", "-r", True, "promisc.pcapng"),
         F_att("fld.aa", "fld.aa", "-a", False, "")]),
    "btle.adv": Spec("ubertooth-btle", ["-n"],
        [F_att("fld.out_opt", "fld.out_opt", "-r", False, "")]),
    "btle.faux": Spec("ubertooth-btle", ["-s"],
        [F_att("fld.bdaddr", "fld.bdaddr", "-s")],
        note_key="note.faux"),
    "btle.interfere": Spec("ubertooth-btle", ["-f", "-I"],
        [F_att("fld.target", "fld.target", "-t", False, "")],
        note_key="note.interfere"),
    "btle.crc": Spec("ubertooth-btle", [],
        [F_att("fld.crc", "fld.crc", "-v", True, "1")], timeout=15),
    "btle.set_aa": Spec("ubertooth-btle", [],
        [F_att("fld.aa", "fld.aa", "-a", True, "8e89bed6")], timeout=15),
    "btle.crackle_cap": Spec("ubertooth-btle", ["-f"],
        [F_att("fld.out_pcap", "fld.out_pcap", "-c", True, "crackle.pcap")],
        note_key="note.crackle"),
    "btle.le_pcap": Spec("ubertooth-btle", ["-f"],
        [F_att("fld.out_pcap", "fld.out_pcap", "-q", True, "le.pcap")]),
}

# ---------------- Tab 3: Classic BR/EDR ------------------------------------
CLASSIC_CMDS = {
    "classic.survey": Spec("ubertooth-rx", ["-z"],
        [F_sep("fld.t_secs", "fld.t_secs", "-t", True, "30"),
         F_sep("fld.out_opt", "fld.out_opt", "-r", False, "")]),
    "classic.follow": Spec("ubertooth-rx", [],
        [F_sep("fld.lap", "fld.lap", "-l"),
         F_sep("fld.uap", "fld.uap", "-u", False, ""),
         F_sep("fld.t_opt", "fld.t_opt", "-t", False, ""),
         F_sep("fld.ch", "fld.ch", "-c", False, ""),
         F_sep("fld.err", "fld.err", "-e", False, "2"),
         F_sep("fld.out_opt", "fld.out_opt", "-r", False, "")]),
    "classic.offline": Spec("ubertooth-rx", [],
        [F_sep("fld.inp", "fld.inp", "-i"),
         F_sep("fld.out_opt", "fld.out_opt", "-r", False, "")]),
    "classic.clk_follow": Spec("ubertooth-follow", [],
        [F_att("fld.lap", "fld.lap", "-l"),
         F_att("fld.uap", "fld.uap", "-u"),
         F_att("fld.out_opt", "fld.out_opt", "-r", False, ""),
         F_sep("fld.err", "fld.err", "-e", False, ""),
         F_sep("fld.hci", "fld.hci", "-b", False, "hci0"),
         F_sep("fld.w", "fld.w", "-w", False, ""),
         F_flag("chk.afh", "chk.afh", "-a")]),
    "classic.afh": Spec("ubertooth-afh", [],
        [F_sep("fld.lap", "fld.lap", "-l"),
         F_sep("fld.uap", "fld.uap", "-u"),
         F_sep("fld.m", "fld.m", "-m", False, "5"),
         F_sep("fld.t_opt", "fld.t_opt", "-t", False, ""),
         F_flag("chk.repeat", "chk.repeat", "-r")]),
    "classic.scan": Spec("ubertooth-scan", [],
        [F_flag("chk.inquiry", "chk.inquiry", "-s"),
         F_flag("chk.extended", "chk.extended", "-x"),
         F_sep("fld.t_secs", "fld.t_secs", "-t", False, "20"),
         F_sep("fld.hci", "fld.hci", "-b", False, "hci0")],
        note_key="note.scan"),
}

# ---------------- Tab 4: Spektrum & Rohdaten -------------------------------
SPECTRUM_CMDS = {
    "spec.sweep": Spec("ubertooth-specan", [],
        [F_sep("fld.lo", "fld.lo", "-l", False, "2402"),
         F_sep("fld.hi", "fld.hi", "-u", False, "2480"),
         F_sep("fld.out_dat", "fld.out_dat", "-d", False, "")]),
    "spec.feed": Spec("ubertooth-specan", ["-g"],
        [F_sep("fld.lo", "fld.lo", "-l", False, "2402"),
         F_sep("fld.hi", "fld.hi", "-u", False, "2480"),
         F_sep("fld.out_dat", "fld.out_dat", "-d", False, "")],
        note_key="note.feed"),
    "spec.feed3d": Spec("ubertooth-specan", ["-G"],
        [F_sep("fld.out_dat", "fld.out_dat", "-d", False, "")]),
    "spec.gui": Spec("ubertooth-specan-ui", [], note_key="note.specan_ui"),
    "spec.dump_c": Spec("ubertooth-dump", ["-c"],
        [F_sep("fld.bin_file", "fld.bin_file", "-d", True, "classic.bin"),
         F_flag("chk.bits", "chk.bits", "-b")]),
    "spec.dump_l": Spec("ubertooth-dump", ["-l"],
        [F_sep("fld.bin_file", "fld.bin_file", "-d", True, "ble.bin"),
         F_flag("chk.bits", "chk.bits", "-b")]),
    "spec.debug": Spec("ubertooth-debug", [],
        [F_sep("fld.reg", "fld.reg", "-r", True, "%manor"),
         F_sep("fld.verb", "fld.verb", "-v", False, "1")], timeout=15),
}

# ---------------- Tab 5: Firmware ------------------------------------------
FIRMWARE_CMDS = {
    "fw.write": Spec("ubertooth-dfu", [],
        [F_sep("fld.dfu_file", "fld.dfu_file", "-d", True, "bluetooth_rxtx.dfu"),
         F_flag("chk.reset", "chk.reset", "-r")],
        note_key="note.dfu"),
    "fw.read": Spec("ubertooth-dfu", [],
        [F_sep("fld.dfu_out", "fld.dfu_out", "-u", True, "backup.dfu")]),
    "fw.suffix": Spec("ubertooth-dfu", [],
        [F_sep("fld.bin_file", "fld.bin_file", "-s", True, "")]),
}

# ---------------- Tab 6: Analyse & Workflow ---------------------------------
ANALYSE_CMDS = {
    "an.crackle_check": Spec("crackle", [],
        [F_sep("fld.pcap_in", "fld.pcap_in", "-i", True, "crackle.pcap")],
        note_key="note.crackle_check"),
    "an.crackle_crack": Spec("crackle", [],
        [F_sep("fld.pcap_in", "fld.pcap_in", "-i", True, "crackle.pcap"),
         F_sep("fld.pcap_out", "fld.pcap_out", "-o", True, "decrypted.pcap")]),
    "an.crackle_ltk": Spec("crackle", [],
        [F_sep("fld.pcap_in", "fld.pcap_in", "-i"),
         F_sep("fld.pcap_out", "fld.pcap_out", "-o"),
         F_sep("fld.ltk", "fld.ltk", "-l")]),
    "an.pipe": Spec("ubertooth-btle", ["-f", "-c", FIFO],
        pre=["rm -f %s && mkfifo %s" % (FIFO, FIFO)],
        post=["rm -f %s" % FIFO],
        note_key="note.pipe"),
    "an.open": Spec("wireshark", [],
        [F_sep("fld.file", "fld.file", "", True, "")], detach=True),
    "an.tshark": Spec("tshark", ["-r"],
        [F_sep("fld.file", "fld.file", "", True, "")], timeout=30),
}

TABS = [
    ("tab.device",   UTIL_CMDS),
    ("tab.ble",      BTLE_CMDS),
    ("tab.classic",  CLASSIC_CMDS),
    ("tab.spectrum", SPECTRUM_CMDS),
    ("tab.firmware", FIRMWARE_CMDS),
    ("tab.analyze",  ANALYSE_CMDS),
]


# ===========================================================================
# 3) GUI
# ===========================================================================
class CommandTab(ttk.Frame):
    """Ein Tab: Combobox + dynamische Felder + Ausführen-Button."""

    def __init__(self, parent, title_key, commands, app):
        super().__init__(parent)
        self.title_key = title_key
        self.commands = commands          # key -> Spec
        self.keys = list(commands.keys())
        self.app = app
        self.current_key = self.keys[0]
        self.widgets = {}                 # feld_key -> (label, widget)
        self.values = {}                  # feld_key -> Variable (aktueller Befehl)
        self.vars_cache = {}              # befehl_key -> {feld_key: Variable}
        self._pending = False             # wird vom App-Manager gesetzt

        top = ttk.Frame(self)
        top.pack(fill=tk.X, pady=4)
        self.cmd_lbl = ttk.Label(top)
        self.cmd_lbl.pack(side=tk.LEFT)
        self.cmd_var = tk.StringVar()
        self.combo = ttk.Combobox(top, textvariable=self.cmd_var,
                                  state="readonly", width=48)
        self.combo.pack(side=tk.LEFT, padx=6)
        self.combo.bind("<<ComboboxSelected>>", self._on_select)

        self.fields = ttk.Frame(self)
        self.fields.pack(fill=tk.X, pady=4)
        self.note_lbl = ttk.Label(self, foreground="#8a6d1a",
                                  wraplength=800, justify=tk.LEFT)
        self.note_lbl.pack(fill=tk.X, pady=2)
        self.preview = ttk.Label(self, foreground="#1a5c8a",
                                 wraplength=800, justify=tk.LEFT)
        self.preview.pack(fill=tk.X, pady=2)

        btns = ttk.Frame(self)
        btns.pack(fill=tk.X, pady=6)
        self.run_btn = ttk.Button(btns, command=lambda: self.app.start(self))
        self.run_btn.pack(side=tk.LEFT, padx=4)

        self.refresh()

    # ----------------------------------------------------------- Auswahl
    def _on_select(self, event=None):
        idx = self.combo.current()
        if 0 <= idx < len(self.keys):
            self.current_key = self.keys[idx]
        self.rebuild_fields()

    def current_spec(self):
        return self.commands[self.current_key]

    # -------------------------------------------------------- Sprache/UI
    def refresh(self):
        """Alle übersetzbaren Texte dieses Tabs aktualisieren."""
        self.cmd_lbl.config(text=tr("ui.command"))
        self.combo["values"] = [tr(k) for k in self.keys]
        if self.current_key in self.keys:
            self.combo.current(self.keys.index(self.current_key))
        self.run_btn.config(text=tr("ui.execute"))
        self.rebuild_fields()

    def rebuild_fields(self):
        for w in self.widgets.values():
            for widget in w:
                if widget is not None:
                    widget.destroy()
        self.widgets.clear()
        self.values.clear()

        spec = self.current_spec()
        cache = self.vars_cache.setdefault(self.current_key, {})
        row = 0
        for key, lkey, flag, style, required, default in spec.fields:
            if key not in cache:
                if style == "flag":
                    cache[key] = tk.BooleanVar(value=bool(default))
                else:
                    cache[key] = tk.StringVar(value=default)
            var = cache[key]
            self.values[key] = var

            if style == "flag":
                lbl = None
                wid = ttk.Checkbutton(self.fields, text=tr(lkey), variable=var)
            else:
                lbl = ttk.Label(self.fields, text=tr(lkey) + ":")
                wid = ttk.Entry(self.fields, textvariable=var, width=44)
            if lbl is not None:
                lbl.grid(row=row, column=0, sticky=tk.W, padx=4, pady=2)
                wid.grid(row=row, column=1, sticky=tk.W, padx=4)
            else:
                wid.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=4)
            self.widgets[key] = (lbl, wid)
            row += 1

        self.note_lbl.config(text=("ℹ " + tr(spec.note_key)) if spec.note_key else "")
        self.update_preview()

    def update_preview(self):
        try:
            argv = self.app.build_argv(self)
            self.preview.config(text=tr("ui.preview") + " " + " ".join(argv))
        except Exception:
            self.preview.config(text=tr("ui.preview") + " –")


class UbertoothApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x740")
        self.root.minsize(780, 620)

        self.proc = None
        self.running = False
        self.active_tab = None
        self.msg_q = queue.Queue()
        self.stop_timer = None
        self._texts = []                    # (widget, key) für Sprachumschaltung

        # Sprachpakete aus dem langs/-Ordner automatisch laden
        self.lang_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "langs")
        TR.load_dir(self.lang_dir)

        self.root.title(tr("app.title"))

        # Statusleiste
        self.status_var = tk.StringVar(value=tr("ui.status_init"))
        ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN,
                  anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

        main = ttk.Frame(root, padding=6)
        main.pack(fill=tk.BOTH, expand=True)

        # ---------- Einstellungsleiste ------------------------------------
        cfg = ttk.LabelFrame(main, padding=4)
        cfg.pack(fill=tk.X)
        self._bind(ttk.Label(cfg), "ui.settings").pack(side=tk.LEFT, padx=4)

        self._bind(ttk.Label(cfg), "ui.language").pack(side=tk.LEFT, padx=(10, 2))
        self.lang_codes = [c for c, _ in TR.available()]
        self.lang_var = tk.StringVar()
        self.lang_combo = ttk.Combobox(
            cfg, textvariable=self.lang_var, state="readonly", width=18,
            values=[f"{p['name']} ({c})" for c, p in TR.available()])
        self.lang_combo.pack(side=tk.LEFT, padx=2)
        if TR.current in self.lang_codes:
            self.lang_combo.current(self.lang_codes.index(TR.current))
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language)

        ttk.Button(cfg, text=tr("ui.load_pack"),
                   command=self.load_pack).pack(side=tk.LEFT, padx=4)
        ttk.Button(cfg, text=tr("ui.export_template"),
                   command=self.export_template).pack(side=tk.LEFT, padx=4)

        self._bind(ttk.Label(cfg), "ui.device_index").pack(side=tk.LEFT, padx=(14, 2))
        self.dev_idx = tk.StringVar(value="0")
        ttk.Entry(cfg, textvariable=self.dev_idx, width=3).pack(side=tk.LEFT)

        self.reset_var = tk.BooleanVar(value=True)
        self._bind(ttk.Checkbutton(cfg, variable=self.reset_var),
                   "ui.reset_radio").pack(side=tk.LEFT, padx=10)

        self._bind(ttk.Label(cfg), "ui.auto_stop").pack(side=tk.LEFT, padx=(4, 2))
        self.autostop = tk.StringVar(value="0")
        ttk.Entry(cfg, textvariable=self.autostop, width=5).pack(side=tk.LEFT)

        ttk.Button(cfg, text=tr("ui.copy"),
                   command=self.copy_command).pack(side=tk.RIGHT, padx=4)
        ttk.Button(cfg, text=tr("ui.export_log"),
                   command=self.export_log).pack(side=tk.RIGHT, padx=4)
        self.stop_btn = ttk.Button(cfg, text=tr("ui.stop"),
                                   command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.RIGHT, padx=4)

        # ---------- Notebook mit Tabs --------------------------------------
        self.nb = ttk.Notebook(main)
        self.nb.pack(fill=tk.BOTH, expand=True, pady=4)
        self.tabs = []
        for title_key, cmds in TABS:
            tab = CommandTab(self.nb, title_key, cmds, self)
            self.nb.add(tab, text=tr(title_key))
            self.tabs.append(tab)

        # ---------- Log-Ausgabe --------------------------------------------
        logf = ttk.LabelFrame(main, padding=4)
        logf.pack(fill=tk.BOTH, expand=True, pady=4)
        self._bind(ttk.Label(logf), "ui.output").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(logf, height=9,
                                                  state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.root.after(150, self.init_device)
        self.root.after(100, self._poll_queue)

    # ----------------------------------------------------------- Text-Bindung
    def _bind(self, widget, key):
        """Widget für Live-Sprachumschaltung registrieren."""
        widget.config(text=tr(key))
        self._texts.append((widget, key))
        return widget

    def _apply_texts(self):
        for w, k in self._texts:
            w.config(text=tr(k))

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

    # ----------------------------------------------------------- Gerät
    def init_device(self):
        try:
            require_root()
            missing = [t for t in ALL_TOOLS if not have(t)]
            if missing:
                self.log(tr("log.missing_tools").format(tools=", ".join(missing)),
                         "WARN")
            out, rc = run_sync(["ubertooth-util", "-v"], timeout=10)
            if rc != 0:
                raise RuntimeError(f"ubertooth-util -v: {out}")
            self.log(tr("log.device_ok").format(fw=out), "OK")
            self.status_var.set(tr("ui.status_ready"))
        except Exception as e:
            self.log(tr("log.init_failed").format(err=e), "ERROR")
            self.status_var.set(tr("ui.status_error"))

    # ------------------------------------------------------- Sprachumschaltung
    def _on_language(self, event=None):
        idx = self.lang_combo.current()
        if 0 <= idx < len(self.lang_codes):
            TR.current = self.lang_codes[idx]
        self.root.title(tr("app.title"))
        self._apply_texts()
        for tab in self.tabs:
            self.nb.tab(tab, text=tr(tab.title_key))
            tab.refresh()
        miss = TR.missing_count()
        if not self.running:
            self.status_var.set(tr("ui.status_ready"))
        self.log(tr("log.lang_changed").format(name=TR.packs[TR.current]["name"]))
        if miss:
            self.log(tr("log.missing_keys").format(n=miss), "WARN")

    def _rebuild_lang_list(self, select_code=None):
        self.lang_codes = [c for c, _ in TR.available()]
        self.lang_combo["values"] = [f"{p['name']} ({c})"
                                     for c, p in TR.available()]
        if select_code and select_code in self.lang_codes:
            self.lang_combo.current(self.lang_codes.index(select_code))
        elif TR.current in self.lang_codes:
            self.lang_combo.current(self.lang_codes.index(TR.current))

    def load_pack(self):
        path = filedialog.askopenfilename(
            title=tr("ui.load_pack"), filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            code = TR.load_file(path)
            self._rebuild_lang_list(select_code=code)
            TR.current = code
            self._on_language()
            self.log(tr("log.pack_loaded").format(name=TR.packs[code]["name"]))
        except Exception as e:
            self.log(tr("log.pack_invalid").format(err=e), "ERROR")

    def export_template(self):
        path = filedialog.asksaveasfilename(
            title=tr("ui.export_template"), defaultextension=".json",
            initialfile="language_template.json",
            filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            TR.export_template(path)
            self.log(tr("log.exported").format(path=path), "OK")
        except Exception as e:
            self.log(tr("log.pack_invalid").format(err=e), "ERROR")

    # ------------------------------------------------------- Befehl bauen
    def build_argv(self, tab):
        spec = tab.current_spec()
        argv = [spec.tool]
        if spec.tool in UBERTOOTH_TOOLS:
            idx = self.dev_idx.get().strip() or "0"
            argv.append("-U" + idx)
        argv += list(spec.base)
        for key, lkey, flag, style, required, default in spec.fields:
            var = tab.values.get(key)
            if var is None:
                continue
            if style == "flag":
                if var.get():
                    argv.append(flag)
                continue
            val = var.get().strip()
            if required and not val:
                raise ValueError(tr("log.field_missing").format(label=tr(lkey)))
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
            self.log(tr("log.running_blocked"), "WARN")
            return
        spec = tab.current_spec()
        try:
            argv = self.build_argv(tab)
        except ValueError as e:
            self.log(str(e), "ERROR")
            return

        for shell_cmd in spec.pre:
            self.log(tr("log.pre").format(cmd=shell_cmd), "INFO")
            subprocess.run(shell_cmd, shell=True, check=False)

        self.running = True
        self.active_tab = tab
        for t in self.tabs:
            t.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set(tr("ui.status_running").format(cmd=" ".join(argv)))
        self.log(tr("log.executing").format(cmd=" ".join(argv)), "INFO")

        try:
            if spec.detach:
                subprocess.Popen(argv, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 start_new_session=True)
                self.log(tr("log.detached"), "OK")
                self._finished()
                return
            self.proc = subprocess.Popen(
                argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, start_new_session=True)
        except FileNotFoundError:
            self.log(tr("log.tool_missing").format(tool=spec.tool), "ERROR")
            self._finished()
            return

        threading.Thread(target=self._reader, daemon=True).start()

        # Auto-Stopp
        try:
            secs = int(self.autostop.get())
            if secs > 0:
                self.stop_timer = threading.Timer(secs, self.stop)
                self.stop_timer.daemon = True
                self.stop_timer.start()
                self.log(tr("log.auto_stop").format(secs=secs), "INFO")
        except ValueError:
            pass
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
                self.msg_q.put(("OK", tr("log.finished_ok")))
            elif rc in (-signal.SIGTERM, -signal.SIGKILL):
                self.msg_q.put(("WARN", tr("log.stopped_sig")))
            else:
                self.msg_q.put(("ERROR", tr("log.failed_rc").format(rc=rc)))
        except Exception as e:
            self.msg_q.put(("ERROR", tr("log.reader_error").format(err=e)))
        finally:
            self.root.after(0, self._finished)

    # --------------------------------------------------------------- Stopp
    def stop(self):
        if self.stop_timer and self.stop_timer.is_alive():
            self.stop_timer.cancel()
        if not self.running or not self.proc:
            return
        self.log(tr("log.stop_sigterm"), "WARN")
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass

        def hard_kill():
            try:
                if self.proc and self.proc.poll() is None:
                    os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)
                    self.msg_q.put(("WARN", tr("log.stop_sigkill")))
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
        self.stop_btn.config(state=tk.DISABLED)
        if spec and spec.post:
            threading.Thread(target=self._run_post, args=(spec.post,),
                             daemon=True).start()
        if spec and spec.tool in UBERTOOTH_TOOLS \
                and spec.tool != "ubertooth-util" and self.reset_var.get():
            threading.Thread(target=self._reset_radio, daemon=True).start()
        self.proc = None
        self.active_tab = None
        self.status_var.set(tr("ui.status_ready"))

    def _run_post(self, cmds):
        for c in cmds:
            self.msg_q.put(("INFO", tr("log.post").format(cmd=c)))
            subprocess.run(c, shell=True, check=False)

    def _reset_radio(self):
        self.msg_q.put(("INFO", tr("log.reset_radio")))
        run_sync(["ubertooth-util", "-S"], timeout=5)
        run_sync(["ubertooth-util", "-r"], timeout=5)

    # ------------------------------------------------------- Hilfsfunktionen
    def copy_command(self):
        if not self.active_tab:
            self.log(tr("log.no_running"), "WARN")
            return
        argv = self.build_argv(self.active_tab)
        self.root.clipboard_clear()
        self.root.clipboard_append(" ".join(argv))
        self.log(tr("log.copied"), "OK")

    def export_log(self):
        path = filedialog.asksaveasfilename(
            title=tr("ui.export_log"), defaultextension=".log",
            initialfile=f"ubertooth_{datetime.now():%Y%m%d_%H%M%S}.log")
        if not path:
            return
        with open(path, "w") as f:
            f.write(self.log_text.get("1.0", tk.END))
        self.log(tr("log.exported").format(path=path), "OK")


if __name__ == "__main__":
    root = tk.Tk()
    UbertoothApp(root)
    root.mainloop()
