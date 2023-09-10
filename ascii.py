import fetch, platform
sysname = platform.uname()[0]
if sysname == "Linux":
    try:
        import distro
    except ModuleNotFoundError as err:
        print(f"Module '{err.name}' was not found. Please install it with pip")
        os._exit(0) 

ascii_art = {"Windows": 
f"""{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################
{fetch.colors.get("blue")}################  ################{fetch.colors.get("reset")}"""}

def insertInfo(sysname, info):
    logo = None
    if sysname == "Darwin":
        logo = ascii_art.get("MacOS")
    if sysname == "Windows":
        logo = ascii_art.get("Windows")
    if sysname == "Linux":
        logo = ascii_art.get(distro.name())
        if logo == None:
            logo = ascii_art.get("Linux")
    
    logo_split = logo.split("\n")
    length = max(len(part) for part in logo_split)+5

    padded_logo = [part.ljust(length) for part in logo_split]
    
    for i,v in enumerate(info):
        try:
            padded_logo[i] = f"{padded_logo[i]}{v}"
        except IndexError:
            padded_logo[i] = ""
            padded_logo[i].rjust(length)
            padded_logo[i] = f"{padded_logo[i]}{v}"

    return padded_logo
