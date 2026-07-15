import subprocess


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


argus_banner = """
  ___   _   _  ____  _   _  ____  _____
 / _ \ | | | ||  _ \| | | ||  _ \| ____| | | || | | || |_) | |_| || |_) |  _|
| |_| | | | || | | ||  _ <| |_| ||  _ <|  _|
 \___/ |_| |_||_| |_||_| \_\____/|_| \_\_|
"""
print(argus_banner)
try:
    while True:
        try:
            menu_choice = int(input("[1] start scan\n[2]  exit:\n"))
        except ValueError:
            print("invalid input")
            continue

        if menu_choice == 1:
            to_scan = input("ip to scan? ")
            scan_ip = Scanner(to_scan)

            print("Scanning... please wait...")
            live_hosts = scan_ip.scan()

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
