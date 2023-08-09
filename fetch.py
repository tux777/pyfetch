#!/bin/python3
# W.I.P.

import platform
import subprocess
import os  

sysname = platform.uname()[0]

if sysname == "Linux" or sysname == "Darwin":
    try:
        import distro
    except ModuleNotFoundError as err:
        print(f"Module '{err.name}' was not found. Please install it with pip")
        os._exit(0) 
elif sysname == "Windows":
    try:
        import wmi
    except ModuleNotFoundError as err:
        print(f"Module '{err.name}' was not found. Please install it with pip")
        os._exit(0) 

# Format is "option-name": value, ...
# For an example: "showShellPath": True

# You can enable an option by setting it to true
# Or you can also disable by setting it to false or removing the option altogether.

#options as of right now are:
# showShellPath | Shows the full path to your shell rather than just displaying its name.

options = { "showShellPath": False} # DO NOT REMOVE! ONLY REMOVE THE OPTIONS INSIDE

# Format is explanatory
# For clarification, info can either be None or have custom info that is persistent no matter what.
# Custom info can be of any type (excluding None obviously). 

info = [ # DO NOT REMOVE! ONLY REMOVE THE INFO INSIDE
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
    "white": '\033[0;37m',
    "reset": "\033[0;0m",
}

bold_colors = {
    "black": '\033[1;30m',
    "red": '\033[1;31m',
    "green": '\033[1;32m',
    "yellow": '\033[1;33m',
    "blue": '\033[1;34m',
    "purple": '\033[1;35m',
    "cyan": '\033[1;36m',
    "white": '\033[1;37m',
}

def getInfo(name):
    macosWMs = ["[c]hunkwm", "[K]wm", "[y]abai", "[A]methyst", "[S]pectacle", "[R]ectangle"]
    macosDefaultWM = "Quartz Compositor"
        
        # The changing of the osName from Darwin to MacOS isn't needed at all
    # MacOS is a name that everyone is familiar with
    
    # Base Info
    if name == "Operating System":
        if sysname == "Darwin" or sysname == "Linux":
            osName = distro.name()
            if osName == "Darwin":
                osName = "MacOS"
        if sysname == "Windows":
            osName = wmi.WMI().Win32_OperatingSystem()[0].Caption
        if sysname == "Darwin":
            return f"{osName} {platform.mac_ver()[0]}"
        else:
            return f"{osName}"
        
    elif name == "Hostname":
        hostname = subprocess.check_output("hostname", shell=True, encoding='utf-8').strip()
        return hostname

    elif name == "Window Manager":
        if sysname == "Darwin":
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
        if sysname == "Darwin" or sysname == "Linux":
            shell = os.getenv("SHELL")
            if options.get("showShellPath") == True:
                return shell
            else:
                shell = shell.split("/")
                return shell[len(shell)-1] # Subtract by 1 because index starts at 0
            
    elif name == "CPU":
        if sysname == "Darwin":
            cpu_name = subprocess.check_output("sysctl machdep.cpu.brand_string", shell=True, encoding='utf-8').split()
            cpu_name = f"{cpu_name[1].split('(')[0]} {cpu_name[2].split('(')[0]} {cpu_name[3]} @ {cpu_name[6]}" 
            cores = subprocess.check_output("sysctl machdep.cpu.core_count", shell=True, encoding='utf-8').split()[1]
            return f"{cpu_name}"
        elif sysname == "Linux":
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
        elif sysname == "Windows":
            cpus_wmi = wmi.WMI().Win32_Processor()
            cpus = []
            for cpu in cpus_wmi:
                cpus.append(cpu.Name)
            return cpus

    elif name == "GPU":
        if sysname == "Darwin":
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
        elif sysname == "Linux":
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
        elif sysname == "Windows":
            gpus_wmi = wmi.WMI().Win32_VideoController()
            gpus = []
            for gpu in gpus_wmi:
                gpus.append(gpu.Name)
            return gpus
    
    elif name == "RAM":
        if sysname == "MacOS": 
            ram = subprocess.check_output("system_profiler SPHardwareDataType | grep Memory", shell=True, encoding='utf-8').split()
            ramSize = ram[1]
            ramMeasurement = ram[2]
            ram = f"{ramSize} {ramMeasurement}"
            return ram
        elif sysname == "Linux":
            memory = subprocess.check_output("cat /proc/meminfo | grep MemTotal", shell=True, encoding='utf-8').split()
            del memory[0]
            memorySize = round(int(memory[0])/1000**2)
            memoryMeasurement = "GB"
            memory = f"{memorySize} {memoryMeasurement}"
            return memory
        elif sysname == "Windows":
            memory = 0
            for stick in wmi.WMI().Win32_PhysicalMemory():
                memory += int(stick.Capacity) / 1024**3
            memory = str(memory).split(".")[0]
            return f"{memory} GB"
            
    
    else:
        return None

for information in info:
    name = information.get("name")
    info = information.get("info")
    enabled = information.get("enabled")

    bold_blue = bold_colors.get("blue")
    reset = colors.get("reset")

    if enabled == True:
        if info == None: 
            returnedInfo = getInfo(name)
            if type(returnedInfo) is str:
                print(f"{bold_blue}{name}: {reset}{returnedInfo}")
            elif type(returnedInfo) is list:
                if len(returnedInfo) == 1:
                    print(f"{bold_blue}{name}: {reset}{returnedInfo[0]}")
                elif len(returnedInfo) > 1:
                    counter = 0
                    for i in returnedInfo:
                        counter += 1
                        print(f"{bold_blue}{name} {counter}: {reset}{returnedInfo[counter-1]}")   
        else:
            print(f"{bold_blue}{name}: {reset}{info}") # If info is present within the info, just print the info instead rather than trying to fetch it in the getInfo function