#!/bin/python3
# W.I.P.

import platform
import subprocess
import os  

try:
   import distro
except ModuleNotFoundError as err:
    print(f"Module '{err.name}' was not found. Please install it with pip")
    os._exit(0)

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
    osName = distro.name()
    if osName == "Darwin":
        osName = "MacOS"
    
    macosWMs = ["[c]hunkwm", "[K]wm", "[y]abai", "[A]methyst", "[S]pectacle", "[R]ectangle"]
    macosDefaultWM = "Quartz Compositor"


    # Base Info
    if name == "Operating System":
        if osName == "MacOS":
            return f"{osName} {platform.mac_ver()[0]}"
        elif osName == "Windows":
            return f"{osName} {platform.win32_ver()[0]}"
        else:
            return f"{osName} {distro.version()}"
        
    elif name == "Hostname":
        if osName == "MacOS":
            return subprocess.check_output("scutil --get ComputerName", shell=True, encoding='utf-8').strip()
        elif osName == "Windows":
            return subprocess.check_output("powershell hostname", shell=True, encoding='utf-8').strip()
        else:
            return subprocess.check_output("cat /etc/hostname", shell=True, encoding='utf-8').strip()
    
    elif name == "Window Manager":
        if osName == "MacOS":
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
        if osName == "MacOS":
            cpu_name = subprocess.check_output("sysctl machdep.cpu.brand_string", shell=True, encoding='utf-8').split()
            cpu_name = f"{cpu_name[1].split('(')[0]} {cpu_name[2].split('(')[0]} {cpu_name[3]} @ {cpu_name[6]}" 
            cores = subprocess.check_output("sysctl machdep.cpu.core_count", shell=True, encoding='utf-8').split()[1]
            return f"{cpu_name}"
        else:
            cpu_name = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | tail -n 1", shell=True, encoding='utf-8').split()
            del cpu_name[0]
            del cpu_name[0]
            del cpu_name[0]
            

            counter = 0
            for i in cpu_name:
                if counter == 0:
                    cpu_name = i
                else:
                    cpu_name = f"{cpu_name} {i}"
                counter+=1

            return cpu_name

    elif name == "GPU":
        if osName == "MacOS":
            gpu_name = subprocess.check_output("system_profiler SPDisplaysDataType | grep Chipset", shell=True, encoding='utf-8').split()
            vram = subprocess.check_output("system_profiler SPDisplaysDataType | grep VRAM", shell=True, encoding='utf-8').split()
            del gpu_name[0]
            del gpu_name[0]
            del vram[0]
            del vram[0]
            del vram[0]


            gpu = ""
            vram = f"{vram[0]} {vram[1]}"

            counter = 0

            for i in gpu_name:
                if counter == 0:
                    gpu = i
                else:
                    gpu = f"{gpu} {i}"

                counter+=1

            gpu_name = f"{gpu} ({vram})" # Insert VRAM amount in string

            return gpu_name
        else:
            if subprocess.check_output("lspci | grep -c VGA", shell=True, encoding='utf-8').split()[0] == "1":
                before_split = subprocess.check_output("lspci | grep VGA", shell=True, encoding='utf-8')
                gpu_name = subprocess.check_output("lspci | grep VGA", shell=True, encoding='utf-8').split()

                counter = 0
                stuffToRemove = ["VGA", ":", "compatible", "Corporation", "Integrated", "Graphics", "Controller", "(rev", "01)", "02)", "03)", "04)", "05)", "06)", "07)", "08)", "09)"] # I don't know how many rev ids there are

                for i,v in enumerate(stuffToRemove):
                    for j in gpu_name:
                        if v in j:
                            gpu_name.remove(j)

                gpu = ""

                counter = 0
                for i in gpu_name:
                    if counter == 0:
                        gpu = i
                    else:
                        gpu = f"{gpu} {i}"
                    counter += 1

                return gpu
    
    elif name == "RAM":
        if osName == "MacOS": 
            ram = subprocess.check_output("system_profiler SPHardwareDataType | grep Memory", shell=True, encoding='utf-8').split()
            ramSize = ram[1]
            ramMeasurement = ram[2]
            ram = f"{ramSize} {ramMeasurement}"
            return ram
        else:
            memory = subprocess.check_output("cat /proc/meminfo | grep MemTotal", shell=True, encoding='utf-8').split()
            del memory[0]
            memorySize = round(int(memory[0])/1000**2)
            memoryMeasurement = "GB"
            memory = f"{memorySize} {memoryMeasurement}"
            return memory
            
    
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
