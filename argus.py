from banner import BANNER
from scanner import (HostScanner,get_network,print_port_results,resolve_host,scan_ports_on_host,COMMON_PORTS, get_port, save_results)
import time
import argparse

parser = argparse.ArgumentParser(description="Argus - Network and Port Scanner", usage="python3 argus.py -t <target>")
parser.add_argument("-t", "--target", help="network or host to scan")
if __name__ == "__main__":
    args = parser.parse_args()

    if args.target:
        if "/" in args.target:
            live_hosts = HostScanner(args.target).scan()
            if not live_hosts:
                print("no ips are up! ")
            else:
                for position,host in enumerate(live_hosts, start=1):
                    print(f"[{position}] {host}")
        else:
            cmd_single_scan = scan_ports_on_host(args.target, COMMON_PORTS)
            print_port_results(cmd_single_scan, args.target)

    else:
        print(BANNER)
        try:
            while True:
                try:
                    print("Welcome to Argus! Please select an option:")
                    menu_choice = int(input("[1] start network scan:\n[2] start single host scan:\n[3] exit:\n..."))
                except ValueError:
                    print("invaid input")
                    continue

                if menu_choice == 1:
                    start_scan_time = time.time()
                    to_scan = get_network()
                    scanner = HostScanner(to_scan)

                    print("Scanning... please wait...")
                    live_hosts = scanner.scan()
                    print("\n--- Scan Results ---")

                    if not live_hosts:
                        print("no ips are up! ")
                    else:
                        for position,host in enumerate(live_hosts, start=1):
                            print(f"[{position}] {host}")
                    print("--------------------\n")
                    print(f"Scan completed: {len(live_hosts)} hosts are up!\n")
                    end_scan_time = time.time()
                    elapsed_scan_time = end_scan_time - start_scan_time
                    print(f"scan finished in: {elapsed_scan_time:.1f} seconds")
                    try:
                        scan_choice = int(input("do you want to scan ports on the found hosts?\n[1] yes\n[2] no \n"))
                    except ValueError:
                        print("invalid input")
                        continue

                    if scan_choice == 1:
                        try:
                            choice = int(input("type the number [x] you want to investigate more: "))
                        except ValueError:
                            print("invalid input only numbers! ")
                            continue
                        if 1 <= choice <= len(live_hosts):
                            start_port_time = time.time()
                            picked_target_ip = live_hosts[choice - 1]
                            found_ports = scan_ports_on_host(picked_target_ip, COMMON_PORTS)
                            print(f"you picked {picked_target_ip}")
                            print("Scanning Ports... please wait...\n")
                            print_port_results(found_ports, picked_target_ip)
                            end_port_time = time.time()
                            elapsed_port_time = end_port_time - start_port_time
                            print(f"port scan finished in: {elapsed_port_time:.1f} seconds")
                        else:
                            print("invalid number")

                    elif scan_choice == 2:
                        print("skipping port scan...")
                    else:
                        print("invalid input")
                        continue

                elif menu_choice == 2:
                    while True:
                        to_scan = resolve_host("host to scan (IP or hostname): ")
                        which_ports = input("scan common ports or custom ports?\n[1] common ports\n[2] custom ports\n...")
                        if which_ports == "1":
                            ports = COMMON_PORTS
                        elif which_ports == "2":
                            ports = get_port()
                        else:
                            print("invalid input")
                            continue
                        print("Scanning Ports... please wait...\n")
                        start_single_time = time.time()
                        found_ports = scan_ports_on_host(to_scan, ports)
                        print_port_results(found_ports, to_scan)
                        end_single_time = time.time()
                        elapsed_single_time = end_single_time - start_single_time
                        print(f"port scan finished in: {elapsed_single_time:.1f} seconds")
                        save_question = input("do you want to save your report as json? \n[1] yes\n[2] no\n")
                        if save_question == "1":
                            print("saving and exporting as json...")
                            save_results(to_scan, found_ports)
                        elif save_question == "2":
                            print("not saving...")
                        else:
                            print("invalid input! ")
                        second_scan = input("\ndo you want to scan another host?\n[1] yes\n[2] no\n...")
                        if second_scan == "1":
                            print("starting new scan...")
                        elif second_scan == "2":
                            break
                        else:
                            print("\ninvalid input")
                            break
                elif menu_choice == 3:
                    print("exiting...")
                    break
                else:
                    print("invalid input")

        except KeyboardInterrupt:
            print("\nexiting...")
