import platform
import subprocess
import os  

sysname = platform.uname()[0]

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
        
        # The changing of the osName from Darwin to MacOS isn't needed at all
    # MacOS is a name that everyone is familiar with
    
    # Base Info
    
    # Operating System
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
    
    
    # Hostname
    elif name == "Hostname":
        if sysname == "Linux":
            hostname = subprocess.check_output("echo $hostname", shell=True, encoding='utf-8').strip()
            return hostname
        elif sysname == "Darwin" or sysname == "Windows":
            hostname = subprocess.check_output("hostname", shell=True, encoding='utf-8').strip()
            return hostname
    
    
    # Window Manager
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
            

    # Shell
    elif name == "Shell":
        if sysname == "Darwin" or sysname == "Linux":
            shell = os.getenv("SHELL")
            if options.get("showShellPath") == True:
                return shell
            else:
                shell = shell.split("/")
                return shell[len(shell)-1] # Subtract by 1 because index starts at 0
            
    # CPU        
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

    # GPU
    elif name == "GPU":
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
    
    # RAM
    elif name == "RAM":
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
            memorySize = round(int(memory[0])/1000**2)
            memoryMeasurement = "GB"
            memory = f"{memorySize} {memoryMeasurement}"
            return memory
        elif sysname == "Windows":
            sticks = wmi.WMI().Win32_PhysicalMemory()
            memory = 0
            
            for stick in sticks:
                memory += int(stick.Capacity) / 1024**3
            memory = str(memory).split(".")[0]
            memory = f"{memory} GB"
            
            if options.get("showRAMSpeed"):
                speed = sticks[0].Speed
                memory = f"{memory} ({speed} MHz)"
            
            return memory
            
    
    else:
        return None