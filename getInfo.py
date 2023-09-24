import platform
import subprocess
import os 
from math import floor, ceil

sysname = platform.uname()[0] # Detetct OS

# OS Specific Imports

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

def getInfo(name, options):
    macosWMs = ["[c]hunkwm", "[K]wm", "[y]abai", "[A]methyst", "[S]pectacle", "[R]ectangle"]
    macosDefaultWM = "Quartz Compositor"
    
    # Base Info
    
    match name:
        
        # Operating System
        case "Operating System":
            if sysname == "Linux":
                osName = distro.name()
            if sysname == "Windows":
                return wmi.WMI().Win32_OperatingSystem()[0].Caption
            if sysname == "Darwin":
                return f"{osName} {platform.mac_ver()[0]}"
            else:
                return f"{osName}"
        
        
        # Kernel
        case "Kernel":
            if sysname == "Darwin" or sysname == "Linux":
                kernel = subprocess.check_output("uname -or", shell=True, encoding='utf-8').strip()
                return kernel
            elif sysname == "Windows":
                kernel = subprocess.check_output("powershell \"Get-WmiObject Win32_OperatingSystem | Select-Object -ExpandProperty Version\"", shell=True, encoding='utf-8').strip()
                return kernel
            
        
        # Hostname
        case "Hostname":
            if sysname == "Linux":
                hostname = subprocess.check_output("cat /etc/hostname", shell=True, encoding='utf-8').strip()
                return hostname
            elif sysname == "Darwin" or sysname == "Windows":
                hostname = subprocess.check_output("hostname", shell=True, encoding='utf-8').strip()
                return hostname


        # Window Manager
        case "Window Manager":
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
                            
        
        # Shell
        case "Shell":
            if sysname == "Darwin" or sysname == "Linux":
                shell = os.getenv("SHELL")
                if options.get("showShellPath") == True:
                    return shell
                else:
                    shell = shell.split("/")
                    return shell[len(shell)-1] # Subtract by 1 because index starts at 0


        # CPU
        case "CPU":
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
                
                
        # GPU
        case "GPU":
            if sysname == "Darwin":
                    gpu_name = subprocess.check_output("system_profiler SPDisplaysDataType | grep Chipset", shell=True, encoding='utf-8').split()
                    vram = subprocess.check_output("system_profiler SPDisplaysDataType | grep VRAM", shell=True, encoding='utf-8').split()
            
                    gpu_name.remove("Chipset")
                    gpu_name.remove("Model:")
                    vram.remove("VRAM")
                    vram.remove("(Dynamic,")
                    vram.remove("Max):")


                    gpu = ""
                    vram = f"{vram[0]} {vram[1]}"

                    for i,v in enumerate(gpu_name):
                        if i == 0:
                            gpu = v
                        else:
                            gpu = f"{gpu} {v}"

                    gpu_name = f"{gpu} ({vram})" # Insert VRAM amount in string

                    return gpu_name
            elif sysname == "Linux":
                try:
                    subprocess.check_output("lspci | grep -c VGA", shell=True, encoding='utf-8')
                    before_split = subprocess.check_output("lspci | grep VGA", shell=True, encoding='utf-8')
                    gpu_name = subprocess.check_output("lspci | grep VGA", shell=True, encoding='utf-8').split()

                    counter = 0
                    stuffToRemove = ["VGA", ":", "compatible", "Corporation", "Integrated", "Graphics", "Controller", "(rev"] #"(rev", "01)", "02)", "03)", "04)", "05)", "06)", "07)", "08)", "09)", "a1)"] # I don't know how many rev ids there are

                    for i,v in enumerate(stuffToRemove):
                        for j in gpu_name:
                            if v in j:
                                gpu_name.remove(j)
                    
                    for i,v in enumerate(gpu_name):
                        if v.endswith("]"):
                            gpu_name[i] = f"{gpu_name[i]}\n"
                    
                    del gpu_name[-1] # Delete rev id

                    for i,v in enumerate(gpu_name):
                        if i == 0:
                            gpu = v
                        else:
                            gpu = f"{gpu} {v}"

                    gpu = gpu.split("\n")
                    
                    for i,v in enumerate(gpu):
                        gpu[i] = gpu[i].strip()

                        if v == '':
                            del gpu[i]


                    return gpu
                except subprocess.CalledProcessError as err:
                    return
                
            elif sysname == "Windows":
                gpus_wmi = wmi.WMI().Win32_VideoController()
                gpus = []
                for gpu in gpus_wmi:
                    gpus.append(gpu.Name)
                return gpus
            
        
        # RAM    
        case "RAM":
                if sysname == "Darwin": 
                    ramSticks = subprocess.check_output("system_profiler SPMemoryDataType | Grep Size", shell=True, encoding='utf-8').split("\n")
                    size = 0
            
                    for stick in ramSticks:
                        stick = stick.split()
                        if stick == []:
                            continue
                        else:
                            size += int(stick[1])
            
                    if options.get("showRAMSpeed"):
                        ramSpeed = subprocess.check_output("system_profiler SPMemoryDataType | Grep Speed", shell=True, encoding='utf-8').split("\n")[0].split()
                        ram = f"{size} GB ({ramSpeed[1]} {ramSpeed[2]})"
                        return ram
        
                elif sysname == "Linux":
                    memory = subprocess.check_output("cat /proc/meminfo | grep MemTotal", shell=True, encoding='utf-8').split()
                    del memory[0]
                    memorySize = floor(int(memory[0])/1000**2)
                    memoryMeasurement = "GB"
                    memory = f"{memorySize} {memoryMeasurement}"
                    return memory
        
                elif sysname == "Windows":
                    sticks = wmi.WMI().Win32_PhysicalMemory()
                    memory: float = 0
                    
                    # Get all sticks
                    for stick in sticks:
                        memory += float(stick.Capacity)
                    
                    # Convert bytes to megabytes
                    memory = memory / (1024**3)
                    memory = f"{memory} GB"
            
                    if options.get("showRAMSpeed"):
                        speed = sticks[0].Speed
                        memory = f"{memory} ({speed} MHz)"
            
                    return memory
            
        case _:
            return None
        
if __name__ == '__main__':
    print("Run fetch.py instead")
