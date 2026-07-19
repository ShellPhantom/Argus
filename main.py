import socket
import subprocess

BANNER = """
[0;33;40m ▄▄▄ [0;37;40m [0;33;40m▄▄▄[0;90;1;40m▄[0;33;40m [0;37;40m [0;33;40m ▄[0;93;1;40m▄▄▄[0;37;40m [0;33;40m▄▄ ▄▄[0;37;40m [0;33;40m ▄▄▄[0;90;1;40m▄[0m
[0;93;1;43m▄█[0;93;1;40m▀[0;93;1;43m█▄[0;37;40m [0;93;1;43m██[0;93;1;40m▀[0;93;1;43m██[0;37;40m [0;93;1;43m▄█[0;93;1;40m▀▀▀[0;37;40m [0;93;1;40m██[0;33;40m [0;93;1;40m██[0;37;40m [0;93;1;40m▒█▀▀[0;90;1;40m▀[0m
[0;93;1;43m▓▓[0;93;1;40m▀[0;93;1;43m▒▒[0;37;40m [0;93;1;43m▓▓[0;93;1;40m▀[0;93;1;43m█[0;33;40m▄[0;37;40m [0;93;1;43m▓▓[0;33;40m ▀[0;93;1;43m▒[0;37;40m [0;93;1;43m▓▓[0;33;40m [0;93;1;40m█[0;93;1;43m▀[0;37;40m [0;93;1;40m▀▀[0;93;1;43m▓▓[0;90;1;40m▄[0m
[0;33;40m▀▀ ▀▀[0;37;40m [0;33;40m▀▀ ▀▀[0;37;40m [0;90;1;40m▀[0;33;40m▀▀▀[0;90;1;40m▀[0;37;40m [0;33;40m▀▀▀▀ [0;37;40m [0;90;1;40m▀[0;33;40m▀▀▀[0;90;1;40m▀[0m
"""
COMMON_PORTS = [
    20,
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    119,
    123,
    143,
    161,
    443,
    445,
    3306,
    3389,
    8080,
]


class Scanning_ip:
    def __init__(self, ip_to_scan):
        self.ip_to_scan = ip_to_scan
        self.active_hosts = []

    def scan(self):
        for p in range(1, 255):
            ip = f"{self.ip_to_scan}.{p}"
            result = subprocess.run(
                ["ping", "-c", "1", "-w", "1", ip], capture_output=True
            )
            if result.returncode == 0:
                self.active_hosts.append(ip)
        return self.active_hosts


def validate_ip():
    while True:
        ip_to_validate = input("ip to scan? (format xxx.xxx.x ) ")
        split_ip = ip_to_validate.split(".")
        if len(split_ip) != 3:
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
                print("not valid address")
                break
        if flag:
            return ip_to_validate


def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((ip, port))
    s.close()

    if result == 0:
        return True
    else:
        return False


def scan_ports_on_host(host):
    open_ports = []
    for port in COMMON_PORTS:
        p_scan = scan_port(host, port)
        if p_scan:
            open_ports.append(port)
    return open_ports


if __name__ == "__main__":
    print(BANNER)
    try:
        while True:
            try:
                menu_choice = int(input("[1] start scan\n[2] exit:\n"))
            except ValueError:
                print("invalid input")
                continue

            if menu_choice == 1:
                to_scan = validate_ip()
                scanner = Scanning_ip(to_scan)

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
                    target_ip = input("which host? (enter full ip): ")
                    print("Scanning Ports... please wait...\n")
                    found_ports = scan_ports_on_host(target_ip)

                    if not found_ports:
                        print(f"no open ports found on {target_ip}")
                    else:
                        for port in found_ports:
                            print(f"port {port} is open on {target_ip}")
                elif scan_choice == 2:
                    print("skipping port scan...")
                else:
                    print("invalid input")
                    continue

            elif menu_choice == 2:
                print("exiting...")
                break

            else:
                print("invalid input")
    except KeyboardInterrupt:
        print("\nexiting...")
