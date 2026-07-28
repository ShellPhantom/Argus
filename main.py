from scanner import HostScanner, validate_ip,scan_ports_on_host,print_port_results, resolve_host
from banner import BANNER

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
