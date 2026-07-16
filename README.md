# Argus

**What is Argus?** In Greek mythology, Argus is the hundred-eyed giant who sees everything — and that's exactly what this tool aims to become. Argus is a CLI network scanner that helps with reconnaissance by identifying devices on a network. Right now it only performs host discovery via ping scanning. Device detection, threading, and port scanning are planned for the future. I'm building this to demonstrate my skills in both programming and networking / cybersecurity.

## Features

- **Ping scan:** sends ICMP packets to find active hosts on your network

## How It Works

**The `Scanner` class** is the blueprint for a scan. It holds the target network prefix (`ip_to_scan`) and a list of discovered hosts (`active_hosts`). It builds an IP address for each host from 1 to 254, pings each one, and collects the addresses that respond. The results are printed in a user-friendly format (currently terminal only).


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
[1] start scan --> enter the IP prefix to scan in the format 192.168.x
                   (the tool iterates through hosts 1–254; range can be changed manually)
[2] exit       --> terminate the program
```

## Roadmap

- [x] Host discovery (ping scan)
- [x] Validation of user-input 
- [ ] Port scanning per host
- [ ] Multithreading for faster scans
- [ ] Device/vendor identification (MAC / OUI lookup)
- [ ] Cleaner reporting and result export