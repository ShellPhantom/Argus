import socket
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor

BANNER = """
[0;33;40m ▄▄▄ [0;37;40m [0;33;40m▄▄▄[0;90;1;40m▄[0;33;40m [0;37;40m [0;33;40m ▄[0;93;1;40m▄▄▄[0;37;40m [0;33;40m▄▄ ▄▄[0;37;40m [0;33;40m ▄▄▄[0;90;1;40m▄[0m
[0;93;1;43m▄█[0;93;1;40m▀[0;93;1;43m█▄[0;37;40m [0;93;1;43m██[0;93;1;40m▀[0;93;1;43m██[0;37;40m [0;93;1;43m▄█[0;93;1;40m▀▀▀[0;37;40m [0;93;1;40m██[0;33;40m [0;93;1;40m██[0;37;40m [0;93;1;40m▒█▀▀[0;90;1;40m▀[0m
[0;93;1;43m▓▓[0;93;1;40m▀[0;93;1;43m▒▒[0;37;40m [0;93;1;43m▓▓[0;93;1;40m▀[0;93;1;43m█[0;33;40m▄[0;37;40m [0;93;1;43m▓▓[0;33;40m ▀[0;93;1;43m▒[0;37;40m [0;93;1;43m▓▓[0;33;40m [0;93;1;40m█[0;93;1;43m▀[0;37;40m [0;93;1;40m▀▀[0;93;1;43m▓▓[0;90;1;40m▄[0m
[0;33;40m▀▀ ▀▀[0;37;40m [0;33;40m▀▀ ▀▀[0;37;40m [0;90;1;40m▀[0;33;40m▀▀▀[0;90;1;40m▀[0;37;40m [0;33;40m▀▀▀▀ [0;37;40m [0;90;1;40m▀[0;33;40m▀▀▀[0;90;1;40m▀[0m
"""
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
        result = subprocess.run(self.ping_command + [ip], capture_output=True)
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
    except socket.timeout:
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

def print_port_results(found_ports):
    if not found_ports["open"]:
        print("no ports are open")
    else:
        print("Open ports:")
        for port in found_ports["open"]:
            print(f" {port}")

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


if __name__ == "__main__":
    print(BANNER)
    try:
        while True:
            try:
                menu_choice = int(input("[1] start network scan:\n[2] start single host scan:\n[3] exit:\n..."))
            except ValueError:
                print("invalid input")
                continue

            if menu_choice == 1:
                to_scan = validate_ip(3)
                scanner = HostScanner(to_scan)

                print("Scanning... please wait...")
                live_hosts = scanner.scan()

                print("\n--- Scan Results ---")

                if not live_hosts:
                    print("no ips are up! ")
                else:
                    print(f"{len(live_hosts)} hosts are up!")
                    for host in live_hosts:
                        print(f"ip: {host} is up")
                print("--------------------\n")
                try:
                    scan_choice = int(input("do you want to scan ports on the live hosts?\n[1] yes\n[2] no "))
                except ValueError:
                    print("invalid input")
                    continue
                if scan_choice == 1:
                    target_ip = resolve_host("host to scan (IP or hostname): ")
                    print("Scanning Ports... please wait...\n")
                    found_ports = scan_ports_on_host(target_ip)
                    print_port_results(found_ports)

                elif scan_choice == 2:
                    print("skipping port scan...")
                else:
                    print("invalid input")
                    continue

            elif menu_choice == 2:
                to_scan = resolve_host("host to scan (IP or hostname): ")
                print("Scanning Ports... please wait...\n")
                found_ports = scan_ports_on_host(to_scan)
                print_port_results(found_ports)

            elif menu_choice == 3:
                print("exiting...")
                break
            else:
                print("invalid input")

    except KeyboardInterrupt:
        print("\nexiting...")
