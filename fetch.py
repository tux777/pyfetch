# W.I.P.

import platform
import subprocess
import os

# The dictionary above stores all info / optional info for fetch.
# The dictonarily allows for flexibility and custom info added by the user

info = [
    { "name": "Operating System", "info": None, "enabled": True }, 
    { "name": "Hostname", "info": None, "enabled": True }, 
    { "name": "Window Manager", "info": None, "enabled": True }, 
    { "name": "Shell", "info": None, "enabled": True }, 
    { "name": "CPU", "info": None, "enabled": True }, 
    { "name": "GPU", "info": None, "enabled": True }, 
    { "name": "RAM", "info": None, "enabled": True }
]

colors = {
    "black": '\033[0;30m',
    "red": '\033[0;31m',
    "green": '\033[0;32m',
    "yellow": '\033[0;33m',
    "blue": '\033[0;34m',
    "purple": '\033[0;35m',
    "cyan": '\033[0;36m',
    "white": '\033[0;37m'
}

bold_colors = {
    "black": '\033[1;30m',
    "red": '\033[1;31m',
    "green": '\033[1;32m',
    "yellow": '\033[1;33m',
    "blue": '\033[1;34m',
    "purple": '\033[1;35m',
    "cyan": '\033[1;36m',
    "white": '\033[1;37m'
}

def getInfo(name):
    
    # Get if system is either windows, linux or macos
    system = platform.uname()
    if system.system == "Darwin":
        system.sysname = "MacOS"
    
    macosWMs = ["[c]hunkwm", "[K]wm", "[y]abai", "[A]methyst", "[S]pectacle", "[R]ectangle"]
    macosDefaultWM = "Quartz Compositor"


    # Base Info
    if name == "Operating System":

        if system.sysname == "MacOS":
            return system.sysname + f" {platform.mac_ver()[0]}"
        else:
            return system.sysname + f" {system.version}"
        
    elif name == "Hostname":

        if system.sysname == "MacOS":
            return subprocess.check_output("scutil --get ComputerName", shell=True, encoding='utf-8').strip()
        elif system.sysname == "Linux":
            return subprocess.check_output("cat /etc/hostname", shell=True, encoding='utf-8').strip()
        elif system.sysname == "Windows":
            return subprocess.check_output("powershell hostname", shell=True, encoding='utf-8').strip()
    
    elif name == "Window Manager":

        if system.sysname == "MacOS":
            counter = 0
            for wm in macosWMs:
                counter+=1
                if counter == len(macosWMs):
                    return macosDefaultWM
                else:
                    try:
                        process = subprocess.check_output(f'ps aux | grep "{wm}"', shell=True, encoding='utf-8').strip()
                        return wm
                    except subprocess.CalledProcessError as err:
                        continue
            


    elif name == "Shell":

        return os.getenv("SHELL")

    elif name == "CPU":

        if system.sysname == "MacOS":
            cpu_name = subprocess.check_output("sysctl machdep.cpu.brand_string", shell=True, encoding='utf-8').split()
            cpu_name = f"{cpu_name[1].split('(')[0]} {cpu_name[2].split('(')[0]} {cpu_name[3]} @ {cpu_name[6]}" 
            cores = subprocess.check_output("sysctl machdep.cpu.core_count", shell=True, encoding='utf-8').split()[1]
            return f"{cpu_name}"

    elif name == "GPU":
        
        if system.sysname == "MacOS":
            gpuArray = subprocess.check_output("system_profiler SPDisplaysDataType | grep Chipset", shell=True, encoding='utf-8').split()
            vramArray = subprocess.check_output("system_profiler SPDisplaysDataType | grep VRAM", shell=True, encoding='utf-8').split()
            del gpuArray[0]
            del gpuArray[0]
            del vramArray[0]
            del vramArray[0]
            del vramArray[0]

            global gpu
            gpu = ""
            vram = f"{vramArray[0]} {vramArray[1]}"

            counter = 0

            for i in gpuArray:
                if counter == 0:
                    gpu = i
                else:
                    gpu = f"{gpu} {i}"
                
                counter+=1
            
            gpu = f"{gpu} ({vram})" # Insert VRAM amount in string
            
            return gpu
    
    elif name == "RAM":
        if system.sysname == "MacOS":
                    
                    ramArray = subprocess.check_output("system_profiler SPHardwareDataType | grep Memory", shell=True, encoding='utf-8').split()
                    ramSize = ramArray[1]
                    ramMeasurement = ramArray[2]
                    ram = f"{ramSize} {ramMeasurement}"
                    return ram

    
    else:
        return None

for information in info:
    name = information.get("name")
    info = information.get("info")
    enabled = information.get("enabled")

    bold_blue = bold_colors.get("blue")
    white = colors.get("white")

    if enabled == True:
        if info == None: 
            if name == "Operating System" or name == "Hostname" or name == "Window Manager" or name == "Shell" or name == "CPU" or name == "GPU" or name == "RAM":
                returnedInfo = getInfo(name)
                print(f"{bold_blue}{name}: {white}{returnedInfo}")
        else:
            print(f"{bold_blue}{name}: {white}{info}")
