<img width="882" height="753" alt="Screenshot 2026-08-02 161608" src="https://github.com/user-attachments/assets/3c4868ac-0c02-4f95-b98b-d2d21c6b269d" />


# Ubertooth One – Complete Control GUI

Eine vollständige grafische Oberfläche (Tkinter) für **alle** echten
Ubertooth-Tools: `ubertooth-util`, `ubertooth-btle`, `ubertooth-rx`,
`ubertooth-dump`, `ubertooth-dfu` und mehr. Keine erfundenen Subkommandos –
jeder Button führt ein reales Tool mit korrekten Optionen aus.

> **Hinweis:** `ubertooth-util` hat **keine** Subkommandos (kein
> `classic sniff`, kein `le scan`, kein `hci capture`). Diese GUI verwendet
> ausschließlich die echte Befehlszeilenschnittstelle des `ubertooth`-Pakets.

## Überblick

Der **Ubertooth One** ist ein Open-Source-USB-Gerät zum Empfangen und
Senden im 2,4-GHz-Band (CC2400). Mit der passenden Firmware
(`bluetooth_rxtx`) kann er:

- **Bluetooth Low Energy (BLE)** mitschneiden (Follow-, Promiscuous- und
  Advertising-Modus)
- **Bluetooth Classic (BR/EDR)** überwachen (Piconet-Survey, UAP/LAP/CLK-
  Recovery)
- **Spektralanalysen** des 2,4-GHz-Bands durchführen
- Als **Repeater** und für **Reichweitentests** fungieren
- Über **DFU-Modus** mit eigener Firmware programmiert werden

## Hardware-Voraussetzungen

- Ubertooth One (oder Zero) per USB angeschlossen
- Linux (getestet auf Kali / Debian / Ubuntu)
- Root-Rechte (`sudo`)

## Installation

```bash
# Ubuntu/Debian/Kali
sudo apt install ubertooth ubertooth-firmware libbtbb-dev wireshark

# Oder aus dem Quellcode (empfohlen für aktuelle Firmware):
wget https://github.com/greatscottgadgets/ubertooth/releases/download/2020-12-R1/ubertooth-2020-12-R1.tar.xz
tar -xf ubertooth-2020-12-R1.tar.xz
cd ubertooth-2020-12-R1/host
mkdir build && cd build
cmake .. && make
sudo make install && sudo ldconfig
```

Zusätzlich (optional):
```bash
sudo apt install crackle          # BLE-Schlüssel-Recovery
```

## Start

```bash
sudo python3 ubertooth_gui.py
```

Das GUI prüft beim Start:
1. Root-Rechte
2. Vorhandene Tools (`ubertooth-util`, `ubertooth-btle`, …)
3. Firmware-Version via `ubertooth-util -v`

## Funktionen

| Bereich | Tools | Funktion |
|---|---|---|
| **Gerät** | `ubertooth-util` | Identifikation, Revision, Seriennummer, Reset, DFU-Modus |
| **Konfiguration** | `ubertooth-util` | Kanal, Squelch, LED-Spektrumanalyzer, PA-Level |
| **BLE** | `ubertooth-btle` | Follow-, Promiscuous- und Advertising-Capture als PCAPNG |
| **Classic** | `ubertooth-rx` | BR/EDR-Capture, Piconet-Survey (`-z`) |
| **Rohdaten** | `ubertooth-dump` | Bitstrom-Dump (Classic/BLE) als Binärdatei |
| **Firmware** | `ubertooth-dfu` | Firmware-Write (`-d file.dfu -r`) |
| **Stopp** | `ubertooth-util` | Sauberes Beenden via `-S` / `-r` |

### Alle unterstützten Befehle im Überblick

```bash
# Gerät
ubertooth-util -I                  # LEDs blinken (Gerät finden)
ubertooth-util -v                  # Firmware-Revision
ubertooth-util -V                  # Kompilier-Info
ubertooth-util -b                  # Board-ID
ubertooth-util -s                  # Seriennummer
ubertooth-util -r                  # Voll-Reset
ubertooth-util -S                  # Operation stoppen
ubertooth-util -f                  # In DFU-Modus wechseln

# Funk
ubertooth-util -U<0-7> -c<MHz>     # Kanal setzen (2400–2483)
ubertooth-util -U<0-7> -z<dBm>     # Squelch setzen (z.B. -z-50)
ubertooth-util -U<0-7> -q<1-225>   # LED-Spektrumanalyzer

# BLE-Capture
ubertooth-btle -U<0-7> -f -r out.pcapng           # Verbindungen folgen
ubertooth-btle -U<0-7> -f -t AA:BB:CC:DD:EE:FF -r out.pcapng  # gezielt
ubertooth-btle -U<0-7> -p -r out.pcapng           # Promiscuous
ubertooth-btle -U<0-7> -n -r out.pcapng           # Nur Advertising
ubertooth-btle -U<0-7> -f -c out.pcap             # PPI-Format für crackle

# Classic BR/EDR
ubertooth-rx -U<0-7> -z -t 30                     # Piconet-Survey
ubertooth-rx -U<0-7> -l <LAP> -r out.pcapng -t 60 # Gezielt folgen
ubertooth-rx -U<0-7> -c <0-79> -r out.pcapng      # Fester Kanal

# Rohdaten
ubertooth-dump -U<0-7> -c -d dump.bin             # Classic-Bits
ubertooth-dump -U<0-7> -l -d dump.bin             # BLE-Bits

# Firmware
ubertooth-dfu -U<0-7> -d bluetooth_rxtx.dfu -r    # Firmware flashen
```

## Ausgabe-Dateiformate

| Format | Flag | Verwendung |
|---|---|---|
| PCAPNG | `-r file.pcapng` | Standard, in Wireshark öffnen |
| PCAP (LE-Pseudoheader) | `-q file.pcap` | Kompatibel mit älteren Tools |
| PCAP (PPI) | `-c file.pcap` | **Erforderlich für crackle** (LE-Schlüssel) |
| Binär | `-d file.bin` | Rohdaten (ubertooth-dump) |

## Analysieren mit Wireshark

```bash
# Offline
wireshark capture.pcapng

# Live-Stream (Pipe)
mkfifo /tmp/pipe
sudo ubertooth-btle -f -c /tmp/pipe
# Wireshark → Capture → Options → Manage Interfaces → New → Pipe: /tmp/pipe
```

## BLE-Schlüssel mit crackle extrahieren

```bash
sudo ubertooth-btle -f -c pairing.pcap      # Legacy Pairing mitschneiden
crackle -i pairing.pcap -o decrypted.pcap   # LTK/SMK extrahieren
```

## Mehrere Geräte

Bei mehreren angeschlossenen Uberteeth wählst du den Index mit `-U<0-7>`:

```bash
sudo ubertooth-util -U 1 -v   # Firmware von Gerät #1
```

## Fehlerbehebung

| Problem | Lösung |
|---|---|
| `No Ubertooth device found` | Kabel prüfen, `lsusb` – Vendor ID `1d50:6002`; ggf. `sudo modprobe cdc_acm` |
| `Permission denied` auf `/dev/ttyACM0` | Als `sudo` ausführen oder udev-Regel für die Gruppe `dialout` |
| `ubertooth-util -v` hängt | Gerät hat sich aufgehängt → USB neu einstecken, `sudo ubertooth-util -r` |
| Firmware-Update bricht ab | Manuell in DFU-Modus: Jumper P4 Pin 1+3 (One) bzw. J1 Pin 1+13 (Zero) kurz schließen, dann `ubertooth-dfu -d file.dfu -r` |
| Wireshark zeigt keine BLE-Pakete | Firmware ≥ 2015-07-R1 verwenden; PPI-Format (`-c`) für ältere Analysen |
| Mehrere Geräte werden nicht unterschieden | Explizit `-U <index>` setzen |

## Rechtliches

Der Ubertooth One ist ein legitimes Werkzeug für **Forschung,
Entwicklung und Sicherheitsaudits**. Setze ihn nur auf Geräten ein,
**die dir gehören oder für die du eine ausdrückliche
schriftliche Genehmigung hast**.

**Sende-Funktionen** (`ubertooth-util -t`, Repeater, Interferenz)
können außerhalb lizenzfreier ISM-Grenzen rechtswidrig sein – in
Deutschland gilt die **Funkgerätegesetzgebung (FTEG/EMVG)**. Vor dem
Senden: Rechtslage prüfen!

## Roadmap

- [ ] Live-PCAP in Wireshark über Pipe direkt aus der GUI
- [ ] Integrierte crackle-Analyse
- [ ] Kanal-Sweep-Visualisierung (Spektrogramm)
- [ ] Windows/macOS-Support über Docker (Linux-Tools)

## Lizenz

GPL-3.0 – basierend auf den GPL-Tools von
[greatscottgadgets/ubertooth](https://github.com/greatscottgadgets/ubertooth).

## Danksagung

- [Project Ubertooth](https://github.com/greatscottgadgets/ubertooth) –
  Hardware, Firmware und Host-Tools
- [libbtbb](https://github.com/greatscottgadgets/libbtbb) – Basisband-Bibliothek
- [crackle](https://github.com/mikeryan/crackle) – BLE-Schlüssel-Recovery
