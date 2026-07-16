import subprocess

BANNER = """
[0;33;40m ▄▄▄ [0;37;40m [0;33;40m▄▄▄[0;90;1;40m▄[0;33;40m [0;37;40m [0;33;40m ▄[0;93;1;40m▄▄▄[0;37;40m [0;33;40m▄▄ ▄▄[0;37;40m [0;33;40m ▄▄▄[0;90;1;40m▄[0m
[0;93;1;43m▄█[0;93;1;40m▀[0;93;1;43m█▄[0;37;40m [0;93;1;43m██[0;93;1;40m▀[0;93;1;43m██[0;37;40m [0;93;1;43m▄█[0;93;1;40m▀▀▀[0;37;40m [0;93;1;40m██[0;33;40m [0;93;1;40m██[0;37;40m [0;93;1;40m▒█▀▀[0;90;1;40m▀[0m
[0;93;1;43m▓▓[0;93;1;40m▀[0;93;1;43m▒▒[0;37;40m [0;93;1;43m▓▓[0;93;1;40m▀[0;93;1;43m█[0;33;40m▄[0;37;40m [0;93;1;43m▓▓[0;33;40m ▀[0;93;1;43m▒[0;37;40m [0;93;1;43m▓▓[0;33;40m [0;93;1;40m█[0;93;1;43m▀[0;37;40m [0;93;1;40m▀▀[0;93;1;43m▓▓[0;90;1;40m▄[0m
[0;33;40m▀▀ ▀▀[0;37;40m [0;33;40m▀▀ ▀▀[0;37;40m [0;90;1;40m▀[0;33;40m▀▀▀[0;90;1;40m▀[0;37;40m [0;33;40m▀▀▀▀ [0;37;40m [0;90;1;40m▀[0;33;40m▀▀▀[0;90;1;40m▀[0m
"""


class Scanner:
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
                octet  = int(split)
                if octet  > 255 or octet  < 0:
                    flag = False
                    print("each octet must be between 0 and 255")
                    break
            except ValueError:
                flag = False
                print("not valid address")
                break
        if flag:
            return ip_to_validate 

print(BANNER)
try:
    while True:
        try:
            menu_choice = int(input("[1] start scan\n[2]  exit:\n"))
        except ValueError:
            print("invalid input")
            continue

        if menu_choice == 1:
            to_scan = validate_ip()
            scanner = Scanner(to_scan)

            print("Scanning... please wait...")       
            live_hosts = scanner.scan()

            print("\n--- Scan Results ---")

            if not live_hosts:
                print("no ips up! ")
            else:
                for host in live_hosts:
                    print(f"ip: {host} is up")
            print("--------------------\n")

        elif menu_choice == 2:
            print("exiting...")
            break

        else:
            print("invalid input")
except KeyboardInterrupt:
    print("\nexiting...")
