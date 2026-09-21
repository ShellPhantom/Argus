import platform
import socket
import subprocess
import json
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

COMMON_PORTS = [20, 21, 22, 23, 25, 53, 80, 110, 119, 123, 143, 161, 443, 445, 3306, 3389, 8080,]
COMMON_HTTP_PORTS = [80, 8080, 8000, 8008, 81, 82]

class HostScanner:
    def __init__(self, ip_to_scan):
        self.ip_to_scan = ip_to_scan
        self.active_hosts = []
        self.os_to_ping = platform.system()
        if self.os_to_ping == "Windows":
            self.ping_command = ["ping", "-n", "1", "-w", "1000"]
        else:
            self.ping_command = ["ping", "-c", "1", "-W", "1"]

    def scan(self):
        network = ipaddress.ip_network(self.ip_to_scan, strict=False)
        ip_list = [str(host) for host in network.hosts()]
        with ThreadPoolExecutor(max_workers=50) as executor:
            pool_result = executor.map(self.ping_host,ip_list)
            up_hosts = [ips for ips in pool_result if ips is not None]
            self.active_hosts = up_hosts
        return up_hosts

    def ping_host(self, ip):
        result = subprocess.run(self.ping_command + [ip], capture_output=True, check=False)
        if result.returncode == 0:
            return ip

def get_network():
    while True:
        ip_string = input("network to scan? (format xxx.xxx.x/xx): ")
        try:
            ipaddress.ip_network(ip_string, strict=False)
            return ip_string
        except ValueError:
            print("invalid network, please try again")

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        return "open"
    except ConnectionRefusedError:
        return "closed"
    except TimeoutError:
        return "filtered"
    except OSError:
        return "unreachable"
    finally:
        s.close()

def scan_ports_on_host(host, ports):
    results  = {"open": [], "closed": [], "filtered": [], "unreachable": []}
    for port in ports:
        state = scan_port(host, port)
        results[state].append(port)
    return results

def print_port_results(found_ports,ip):
    if not found_ports["open"]:
        print("no ports are open")
    else:
        print("Open ports:")
        for port in found_ports["open"]:
            banner = grab_banner(ip, port)
            if banner:
                print(f" {port} service: {banner}")
            else:
                print(f" {port} service: unknown")

    if not found_ports["filtered"]:
        print("no ports are filtered")

    else:
        print("Filtered ports:")
        for port in found_ports["filtered"]:
            print(f" {port}")

    closed_ports = len(found_ports["closed"])
    print(f"{closed_ports} ports are closed")
    print("--------------------\n")
    print(f"{len(found_ports['open'])} ports are open\n")

    if found_ports["unreachable"]:
        unreachable_ports = len(found_ports["unreachable"])
        print(f"{unreachable_ports} ports are unreachable")

def resolve_host(prompt):
    while True:
        user_input = input(prompt)
        try:
            ip = socket.gethostbyname(user_input)
            return ip
        except socket.gaierror:
            print("invalid hostname, please try again")

def grab_banner(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        if port in COMMON_HTTP_PORTS:
            s.send(b"GET / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024)
        return banner.decode(errors="ignore").strip()
    except (ConnectionRefusedError, TimeoutError, OSError):
        return None
    finally:
        s.close()

def get_single_ports(port_string):
    ports_to_scan = []
    split_ports = port_string.split(",")
    for port in split_ports:
        try:
            port_number = int(port)
            if 1 <= port_number <= 65535:
                ports_to_scan.append(port_number)
            else:
                print(f"{port} is out of range")
        except ValueError:
            print(f"{port} is not a number")
    return ports_to_scan

def get_port():
    while True:
        port_string = input("Which ports you want to scan? (format: x,x,x) ")
        user_ports = get_single_ports(port_string)
        if user_ports:
            return user_ports
        print("invalid ports, please try again")

def save_results(host, found_ports):
    date_now = datetime.now()
    date_name = date_now.strftime("%d-%m-%Y_%H:%M")
    date_time = date_now.strftime("%H:%M")
    json_result = {"scan_time": date_time} | {"host": host} | found_ports
    with open(f"scan_result_{date_name}.json","w") as f:
        json.dump(json_result, f, indent=4)
