# Argus

**What is Argus?** In Greek mythology, Argus is the hundred-eyed giant who sees everything — and that's exactly what this tool aims to become. Argus is a CLI network scanner that helps with reconnaissance by identifying devices on a network. Right now it can perform host discovery via ping scanning, and you can then run port scans on the discovered hosts. Device detection, service fingerprinting and much more are planned for the future.
I'm building this to demonstrate my skills in both programming and networking / cybersecurity.
##


## Disclaimer: For educational purposes and authorized testing only. Only scan systems you own or have permission to test.

## Features

- **Ping scan:** sends ICMP packets to find active hosts on your network
- **Port scan:** scans the most common ports on discovered hosts
- **Hostname support:** accepts a hostname instead of an IP and resolves it to an address before scanning
- **Cross-platform support:** detects the operating system it runs on and uses the matching ping command (currently Windows and Linux)
- **Multithreading:** scans hosts in parallel instead of one after another, which makes network scans much faster
- **Passive Banner Grabbing:** attempts to grab banners from open ports to identify services

## How It Works

**The `HostScanner` class** is the blueprint for a scan. It holds the target network prefix (`ip_to_scan`) and a list of discovered hosts (`active_hosts`). It builds an IP address for each host from 1 to 254, and pings them parallel using a thread poolpings and collects the addresses that respond. The results are printed in a user-friendly format (currently terminal only).

**The port scan** allows you to scan the most common ports on discovered hosts. After host discovery, you can choose to perform a port scan on an active host.

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
python main.py
```

## Usage

Once started, an interactive menu will appear in your console:

```
[1] start network scan --> enter the IP prefix to scan in the format 192.168.x
                           (the tool iterates through hosts 1–254; range can be changed manually)
                           after the host discovery you can choose to scan ports on the discovered hosts
[2] start single host scan --> enter IP or name of a single host to scan for open ports
                    
[3] exit --> terminate the program
```

## Roadmap

- [x] Host discovery (ping scan)
- [x] Validation of user-input 
- [x] Port scanning per host
- [x] DNS resolution for hostnames 
- [x] Multithreading for faster scans
- [ ] Service fingerprinting / banner grabbing
- [ ] Cleaner reporting and result export
- [ ] Device/vendor identification (MAC / OUI lookup)
