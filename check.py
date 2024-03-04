import os
import platform
import subprocess
import sys

def get_os_info():
    print("Operating System Information:")
    print(f"System: {platform.system()}")
    print(f"Node Name: {platform.node()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

def get_python_info():
    print("\nPython Environment Information:")
    print(f"Python Version: {platform.python_version()}")
    try:
        import pip
        installed_packages = pip.get_installed_distributions()
        print("\nInstalled Python Packages:")
        for package in installed_packages:
            print(f"{package.key}=={package.version}")
    except ImportError:
        print("Pip is not available.")

def get_system_libraries_info():
    if platform.system() == "Windows":
        print("\nWindows System Libraries Information: (Limited)")
        # Windows specific commands here
        # For example, using `subprocess` to execute `wmic product get name, version`
    elif platform.system() == "Linux":
        print("\nLinux System Libraries Information: (Limited)")
        # Linux specific commands here
        # For example, using `subprocess` to execute `dpkg --get-selections`
    elif platform.system() == "Darwin":
        print("\nMac System Libraries Information: (Limited)")
        # Mac specific commands here
        # For example, using `subprocess` to execute `system_profiler SPApplicationsDataType`

def main():
    get_os_info()
    get_python_info()
    get_system_libraries_info()

if __name__ == "__main__":
    main()
