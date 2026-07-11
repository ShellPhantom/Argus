import subprocess

# ip = input("Enter the IP address to ping: ")

for p in range(1, 255):
    whole_ip = f"192.168.2.{p}"
    result = subprocess.run(
        ["ping", "-c", "1", "-w", "1", whole_ip], capture_output=True
    )

    if result.returncode == 0:
        print(f"ip: 192.168.2.{p} is up")
