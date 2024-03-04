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

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except subprocess.CalledProcessError:
        print("Failed to execute the command.")
        return ""

def parse_and_print(output, parser):
    apps = parser(output)
    for name, version in apps:
        if name and version:  # Check to avoid printing empty entries
            print(f'"{name}"="{version}"')

def windows_parser(output):
    apps = []
    current_app = {}
    for line in output.split('\n'):
        if "DisplayName" in line:
            current_app['name'] = line.split(':', 1)[1].strip()
        elif "DisplayVersion" in line:
            current_app['version'] = line.split(':', 1)[1].strip()
            if 'name' in current_app and 'version' in current_app:
                apps.append((current_app['name'], current_app['version']))
                current_app = {}
    return apps

def linux_parser(output):
    apps = []
    for line in output.strip().split("\n"):
        parts = line.strip().split()
        if len(parts) >= 2 and parts[0] and parts[1]:  # Ensure both name and version are present
            apps.append((parts[0], parts[1]))
        elif parts and parts[0]:  # Only add if the name is present
            apps.append((parts[0], "Unknown"))
    return apps

def get_system_libraries_info():
    if platform.system() == "Windows":
        print_divider("Windows System Libraries and Applications Information")
        command = 'powershell "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion | Format-List"'
        output = execute_command(command)
        parse_and_print(output, windows_parser)

    elif platform.system() == "Linux":
        print_divider("Linux System Libraries and Applications Information")
        if os.path.isfile("/usr/bin/dpkg"):
            command = 'dpkg -l | awk \'{print $2 " " $3}\''
        elif os.path.isfile("/usr/bin/rpm"):
            command = 'rpm -qa --queryformat "%{NAME} %{VERSION}-%{RELEASE}\n"'
        else:
            print("Unsupported Linux distribution or package manager not found.")
            return
        output = execute_command(command)
        parse_and_print(output, linux_parser)

    elif platform.system() == "Darwin":
        print_divider("Mac System Libraries and Applications Information")
        command = 'system_profiler SPApplicationsDataType | awk -F": " \'/^[ ]+[^:]+: [^ ]/ {app=$1; getline; ver=$2; print app " " ver}\''
        output = execute_command(command)
        parse_and_print(output, linux_parser)

def perform_diagnosis_checks(ports):
    print_divider("Diagnosis Checks")
    # Python PATH check
    python_path = shutil.which("python") or shutil.which("python3")
    print(f"[{'+' if python_path else '-'}] Python in PATH")

    # Port bindability check
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(("localhost", port)) == 0
        print(f"[{'-' if result else '+'}] Port {port} bindable")

    # requirements.txt presence and dependencies check
    requirements_present = os.path.isfile("requirements.txt")
    print(f"[{'+' if requirements_present else '-'}] requirements.txt present")
    if requirements_present:
        with open("requirements.txt") as f:
            required_packages = f.readlines()
        installed_packages = {d.project_name.lower(): d.version for d in pkg_resources.working_set}
        missing_packages = [pkg.split("==")[0].strip().lower() for pkg in required_packages if pkg.split("==")[0].strip().lower() not in installed_packages]
        print(f"[{'+' if not missing_packages else '-'}] All dependencies installed")

    # Disk space check
    _, _, free = shutil.disk_usage(".")
    print(f"[{'+' if free > 1e+9 else '-'}] Sufficient disk space")  # Assuming 1GB is sufficient

    # Write permission check
    write_permission = os.access(".", os.W_OK)
    print(f"[{'+' if write_permission else '-'}] Write permission in current directory")

    # Network connectivity check
    try:
        urllib.request.urlopen("http://www.google.com", timeout=10)
        network_connectivity = True
    except urllib.error.URLError:
        network_connectivity = False
    print(f"[{'+' if network_connectivity else '-'}] Network connectivity")

    # Virtual environment check
    virtual_env = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"[{'+' if virtual_env else '-'}] Virtual environment activated")

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
    get_system_libraries_info()
    perform_diagnosis_checks(ports)

if __name__ == "__main__":
    main()