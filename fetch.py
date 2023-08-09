#!/bin/python3
# W.I.P.

from getInfo import getInfo

# Format is "option-name": value, ...
# For an example: "showShellPath": True

# You can enable an option by setting it to true
# Or you can also disable by setting it to false or removing the option altogether.

#options as of right now are:
# showShellPath | Shows the full path to your shell rather than just displaying its name.

options = { "showShellPath": False } # DO NOT REMOVE! ONLY REMOVE THE OPTIONS INSIDE

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

for information in info:
    name = information.get("name")
    info = information.get("info")
    enabled = information.get("enabled")

    bold_blue = bold_colors.get("blue")
    reset = colors.get("reset")

    if enabled == True:
        if info == None: 
            returnedInfo = getInfo(name, options)
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