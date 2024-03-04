import os
import platform
import subprocess
import sys
import pkg_resources
import shutil
import socket
import urllib.request

def print_divider(title):
    print("\n" + "=" * 50)
    print(f" {title} ")
    print("=" * 50)

def get_os_info():
    print_divider("Operating System Information")
    print(f"System: {platform.system()}")
    print(f"Node Name: {platform.node()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

def get_python_info():
    print_divider("Python Environment Information")
    print(f"Python Version: {platform.python_version()}")
    print("\nInstalled Python Packages:")
    installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
    for project_name, version in sorted(installed_packages):
        print(f'"{project_name}"="{version}"')

def perform_diagnosis_checks(ports):
    print_divider("Diagnosis Checks")
    # Python PATH check
    python_path = shutil.which("python") or shutil.which("python3")
    print(f"Python in PATH: {'✓' if python_path else '✗'}")

    # Port bindability check
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(("localhost", port)) == 0
        print(f"Port {port} bindable: {'✗' if result else '✓'}")

    # requirements.txt presence and dependencies check
    requirements_present = os.path.isfile("requirements.txt")
    print(f"requirements.txt present: {'✓' if requirements_present else '✗'}")
    if requirements_present:
        with open("requirements.txt") as f:
            required_packages = f.readlines()
        installed_packages = {d.project_name.lower(): d.version for d in pkg_resources.working_set}
        missing_packages = [pkg.split("==")[0].strip().lower() for pkg in required_packages if pkg.split("==")[0].strip().lower() not in installed_packages]
        print(f"All dependencies installed: {'✓' if not missing_packages else '✗'}")

    # Disk space check
    _, _, free = shutil.disk_usage(".")
    print(f"Sufficient disk space: {'✓' if free > 1e+9 else '✗'}")  # Assuming 1GB is sufficient

    # Write permission check
    write_permission = os.access(".", os.W_OK)
    print(f"Write permission in current directory: {'✓' if write_permission else '✗'}")

    # Network connectivity check
    try:
        urllib.request.urlopen("http://www.google.com", timeout=10)
        network_connectivity = True
    except urllib.error.URLError:
        network_connectivity = False
    print(f"Network connectivity: {'✓' if network_connectivity else '✗'}")

    # Virtual environment check
    virtual_env = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"Virtual environment activated: {'✓' if virtual_env else '✗'}")

def show_help():
    print("Usage: python checker.py [options]")
    print("Options:")
    print("  -h, /h, --help       Show this help message and exit")
    print("  --ports=PORTS        Specify multiple ports separated by commas to check bindability (e.g., --ports=8000,8080)")

def parse_arguments():
    ports = []
    for arg in sys.argv[1:]:
        if arg in ("-h", "/h", "--help"):
            show_help()
            sys.exit()
        elif arg.startswith("--ports="):
            ports_str = arg[len("--ports="):]
            ports = [int(port.strip()) for port in ports_str.split(",") if port.strip().isdigit()]
        else:
            print(f"Unknown argument: {arg}")
            show_help()
            sys.exit(1)
    return ports

def main():
    ports = parse_arguments()
    get_os_info()
    get_python_info()
    perform_diagnosis_checks(ports)

if __name__ == "__main__":
    main()