# Argus

**What is Argus?** In Greek mythology, Argus is the hundred-eyed giant who sees everything — and that's exactly what this tool aims to become. Argus is a CLI network scanner that helps with reconnaissance by identifying devices on a network. Right now it performs host discovery via ping scanning, port scans on hosts, and active/passive banner grabbing, with CLI arguments for automation and result export as JSON. Device detection and much more are planned for the future.

I'm building this to demonstrate my skills in both programming and networking / cybersecurity.

## Disclaimer: For educational purposes and authorized testing only. Only scan systems you own or have permission to test.

## Whats new in this version?

- Json reporting capabilities
- CLI argument support for automation

## Features

- **Ping scan:** sends ICMP packets to find active hosts on your network
- **Port scan:** scans the most common ports or a user-defined list of ports on discovered hosts
- **Hostname support:** can accept hostnames instead of an IP and resolves it to an address before scanning
- **Cross-platform support:** detects the operating system it runs on and uses the matching ping command (currently Windows and Linux)
- **Multithreading:** scans hosts in parallel instead of one after another, which makes network scans much faster
- **Banner Grabbing:** attempts to grab banners to identify services
- **JSON Report Export:** saves scan results in a structured JSON format for further analysis (first version is a simple list of active hosts and open ports, future versions will include more details)

## How It Works

**The `HostScanner` class** is the blueprint for a scan. It holds the target network in CIDR notation (ip_to_scan) and a list of discovered hosts (active_hosts). It expands the network into its individual host addresses using Python's ipaddress module, pings them in parallel using a thread pool, and collects the addresses that respond. The results are printed to the terminal and can optionally be exported as JSON.

**The port scan** allows you to scan the most common ports or a custom list of ports. 

**DNS resolution** is also supported. If you enter a hostname instead of an IP address, the tool will resolve it to an IP before scanning.

## How to Run

No external dependencies needed — only Python 3.

1. Make sure Python 3 is installed on your system.
2. Clone the repo:
```
git clone https://github.com/ShellPhantom/Argus.git
```
3. Open your terminal and run:
```
python argus.py
```

## Usage

**CLI mode** (for automation):
```
python argus.py -t 192.168.2.0/24    # scan a network
python argus.py -t 192.168.2.1       # scan a single host
python argus.py -h                   # show help
```

**Interactive mode** (no arguments) — a menu appears in your console:
```
[1] start network scan     --> enter the network in CIDR notation (e.g. 192.168.2.0/24)
                               after host discovery you can scan ports on a discovered host
[2] start single host scan --> enter an IP or hostname to scan for open ports
[3] exit                   --> terminate the program
```

## Roadmap

- [x] Port scanning per host
- [x] DNS resolution for hostnames 
- [x] Multithreading for faster scans
- [x] Reporting and result export as json
- [x] Service fingerprinting
- [x] CLI argument support for automation
- [ ] Device/vendor identification (MAC / OUI lookup)
