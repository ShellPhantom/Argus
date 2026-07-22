# Argus

**What is Argus?** In Greek mythology, Argus is the hundred-eyed giant who sees everything — and that's exactly what this tool aims to become. Argus is a CLI network scanner that helps with reconnaissance by identifying devices on a network. Right now it can perform host discovery via ping scanning and now you can do port scans on the discovered hosts. Device detection, threading and much more is planned for the future. 
I'm building this to demonstrate my skills in both programming and networking / cybersecurity.

## Features

- **Ping scan:** sends ICMP packets to find active hosts on your network
- **Port scan:** scans the most common ports on discovered hosts
- **DNS resolution:** Hostname support: accepts a hostname instead of an IP and resolves it to an address before scanning
- **OS detection:** detects the os of the user to ensure the right ping command is used (currently only supports Windows and Linux)

## How It Works

**The `HostScanner` class** is the blueprint for a scan. It holds the target network prefix (`ip_to_scan`) and a list of discovered hosts (`active_hosts`). It builds an IP address for each host from 1 to 254, pings each one, and collects the addresses that respond. The results are printed in a user-friendly format (currently terminal only).

**The port scan** is the new functionality that allows you to scan the most common ports on discovered hosts. After host discovery, you can choose to perform a port scan on an active host.

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
- [ ] Multithreading for faster scans
- [ ] Device/vendor identification (MAC / OUI lookup)
- [ ] Cleaner reporting and result export
