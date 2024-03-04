import os
import platform
import subprocess
import sys
import pkg_resources  # Added for listing installed packages

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
    for line in output.strip().split("\n"):
        name, version = parser(line)
        if name and version:
            print(f'"{name}"="{version}"')

def windows_parser(line):
    try:
        name, version = line.strip().split(",")[0].split("=", 1)
        name = name.replace("DisplayName: ", "").strip()
        version = version.replace("DisplayVersion: ", "").strip()
        return name, version
    except ValueError:
        return None, None

def linux_parser(line):
    parts = line.strip().split()
    if len(parts) >= 2:
        return parts[0], parts[1]
    else:
        return parts[0], "Unknown"

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

def main():
    get_os_info()
    get_python_info()
    get_system_libraries_info()

if __name__ == "__main__":
    main()