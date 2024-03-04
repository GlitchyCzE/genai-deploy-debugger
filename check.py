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

def check_python_path():
    print_divider("Python PATH Check")
    python_path = shutil.which("python") or shutil.which("python3")
    if python_path:
        print(f"Python is in your PATH: {python_path}")
    else:
        print("Python is NOT in your PATH.")

def check_port_bindable(ports):
    for port in ports:
        print_divider(f"Port Bindability Check for Port {port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                print(f"Port {port} is available for binding.")
            except OSError:
                print(f"Port {port} is NOT available for binding. It may be in use or restricted.")

def check_requirements_txt():
    print_divider("requirements.txt Presence Check")
    if os.path.isfile("requirements.txt"):
        print("requirements.txt is present.")
        check_requirements_dependencies()
    else:
        print("requirements.txt is NOT present.")

def check_requirements_dependencies():
    print_divider("requirements.txt Dependencies Check")
    with open("requirements.txt") as f:
        required_packages = f.readlines()
    installed_packages = {d.project_name.lower(): d.version for d in pkg_resources.working_set}
    missing_packages = []
    for package in required_packages:
        package_name = package.split("==")[0].strip().lower()
        if package_name not in installed_packages:
            missing_packages.append(package.strip())
    if missing_packages:
        print("Missing packages from requirements.txt:")
        for package in missing_packages:
            print(f"- {package}")
    else:
        print("All dependencies in requirements.txt are installed.")

def check_disk_space():
    print_divider("Disk Space Check")
    total, used, free = shutil.disk_usage(".")
    print(f"Total: {total // (2**30)} GiB, Used: {used // (2**30)} GiB, Free: {free // (2**30)} GiB")

def check_write_permission():
    print_divider("Write Permission Check")
    if os.access(".", os.W_OK):
        print("You have write permission in the current directory.")
    else:
        print("You do NOT have write permission in the current directory.")

def check_network_connectivity():
    print_divider("Network Connectivity Check")
    try:
        urllib.request.urlopen("http://www.google.com", timeout=10)
        print("Network connectivity is available.")
    except urllib.error.URLError:
        print("Network connectivity is NOT available.")

def check_virtual_env():
    print_divider("Virtual Environment Check")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("A virtual environment is currently activated.")
    else:
        print("No virtual environment is activated.")

def show_help():
    print("Usage: python checker.py [options]")
    print("Options:")
    print("  -h, /h, --help       Show this help message and exit")
    print("  --ports=PORTS        Check port bindability for a list of comma-separated ports (e.g., --ports=8000,8080)")

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
    check_python_path()
    if ports:
        check_port_bindable(ports)
    check_requirements_txt()
    check_disk_space()
    check_write_permission()
    check_network_connectivity()
    check_virtual_env()

if __name__ == "__main__":
    main()