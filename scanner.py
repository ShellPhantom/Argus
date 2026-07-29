import platform
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [20, 21, 22, 23, 25, 53, 80, 110, 119, 123, 143, 161, 443, 445, 3306, 3389, 8080,]

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
        ip_list = [f"{self.ip_to_scan}.{p}" for p in range(1,255) ]
        with ThreadPoolExecutor(max_workers=50) as executor:
            pool_result = executor.map(self.ping_host,ip_list)
            up_hosts = [ips for ips in pool_result if ips is not None]
            self.active_hosts = up_hosts
        return up_hosts

    def ping_host(self, ip):
        result = subprocess.run(self.ping_command + [ip], capture_output=True, check=False)
        if result.returncode == 0:
            return ip

def validate_ip(expected_parts):
    while True:
        ip_to_validate = input("ip to scan? (format xxx.xxx.x or xxx.xxx.xxx.xx) ")
        split_ip = ip_to_validate.split(".")
        if len(split_ip) != expected_parts:
            print("wrong format")
            continue

        flag = True
        for split in split_ip:
            try:
                octet = int(split)
                if octet > 255 or octet < 0:
                    flag = False
                    print("each octet must be between 0 and 255")
                    break
            except ValueError:
                flag = False
                print("not a valid address")
                break
        if flag:
            return ip_to_validate

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

def scan_ports_on_host(host):
    results  = {"open": [], "closed": [], "filtered": [], "unreachable": []}
    for port in COMMON_PORTS:
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
            if
                print(f" {port} service: {grab_banner(ip, port)}")
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
        banner = s.recv(1024)
        return banner.decode(errors="ignore").strip()
    except (ConnectionRefusedError, TimeoutError, OSError):
        return None
    finally:
        s.close()
