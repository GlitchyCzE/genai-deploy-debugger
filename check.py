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
        print(f"{project_name}=={version}")

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = result.stdout
        if output:
            print(output)
        else:
            print("No information available or access denied.")
    except subprocess.CalledProcessError:
        print("Failed to execute the command.")

def get_system_libraries_info():
    if platform.system() == "Windows":
        print_divider("Windows System Libraries and Applications Information")
        # Example command to list installed programs on Windows
        command = 'powershell "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion | Format-List"'
        execute_command(command)

    elif platform.system() == "Linux":
        print_divider("Linux System Libraries and Applications Information")
        # Example command to list installed packages on Debian/Ubuntu
        command = 'dpkg --get-selections | grep -v deinstall'
        execute_command(command)

    elif platform.system() == "Darwin":
        print_divider("Mac System Libraries and Applications Information")
        # Example command to list installed applications on Mac
        command = 'system_profiler SPApplicationsDataType'
        execute_command(command)

def main():
    get_os_info()
    get_python_info()
    get_system_libraries_info()

if __name__ == "__main__":
    main()