import os
import sys
import zoneinfo
import platform
import requests
from datetime import datetime

# Redirect print to file
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        now = datetime.now()
        year = now.year
        month = now.month
        current_date = now.strftime("%Y.%m.%d")
        self.log_dir = f"logs/{year}/{month}"
        os.makedirs(self.log_dir, exist_ok=True)

        self.log = open(os.path.join(self.log_dir, f"{current_date}.log"), "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger()

# Log time
def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

log_current_time = get_current_time()
print(f"\nProgram started at {log_current_time}")

# Get system information
info = [
    f'Operating System Name: {platform.system()}',
    f'Operating System Version: {platform.version()}',
    f'System Architecture: {platform.architecture()}',
    f'Computer Type: {platform.machine()}',
    f'Computer Name: {platform.node()}',
    f'Processor Type: {platform.processor()}',
    f'Python Version: {platform.python_version()}',
    f'Python Interpreter Name: {platform.python_implementation()}'
]
print('\n'.join(info))

#Get CN Bing Wallpaper
log_current_time = get_current_time()
print(f"[{log_current_time}] Start geting CN Bing Wallpaper")
api_url_cn = "https://cn.bing.com/HPImageArchive.aspx?n=1&mkt=zh-cn&idx=0&format=js"
response = requests.get(api_url_cn)
if response.status_code == 200:
    #save image
    data = response.json()
    urlbase = data["images"][0]["urlbase"]
    url = "https://www.bing.com" + urlbase + "_UHD.jpg"
    log_current_time = get_current_time()
    print(f"[{log_current_time}] Successful get url: {url}")
    image_data = requests.get(url).content
    image_path = os.path.join("img", "background.jpg")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(image_data)
        f.close()
    log_current_time = get_current_time()
    print(f"[{log_current_time}] Image saved to {image_path}")
    #Get image info
    enddate = data["images"][0]["enddate"]
    yy = f"{enddate[:4]}"
    mm = f"{enddate[4:6]}"
    dd = f"{enddate[6:]}"
    enddate = f"{enddate[:4]}-{enddate[4:6]}-{enddate[6:]}"
    copy = data["images"][0]["copyright"]
    title = data["images"][0]["title"]
    #write README.md
    info_path = os.path.join("README.md")
    with open(info_path, "w", encoding='utf-8') as f:
        f.write(f"## Today's Bing Wallpaper\n")
        f.write(f"Update: {enddate}\n")
        f.write(f"![]({url}&w=1000)Download: [{copy}]({url})")
        f.write(f"\n\nAuto get programm by LtgX\n")
    log_current_time = get_current_time()
    print(f"[{log_current_time}] Info saved to {info_path}")
    #write backup markdown
    history_file_name = f"{dd}.md"
    history_path = os.path.join("history",yy,mm,history_file_name)
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding='utf-8') as f:
        f.write(f"## History Bing Wallpaper\n")
        f.write(f"Wallpaper date: {enddate}\n")
        f.write(f"![]({url}&w=1000)Download: [{copy}]({url})")
        f.write(f"\n\nAuto get programm by LtgX\n")
    log_current_time = get_current_time()
    print(f"[{log_current_time}] Image saved to {history_path}")
else:
    log_current_time = get_current_time()
    print(f"[{log_current_time}] Failed with response code: {response.status_code}")


#Get Blobal Bing Wallpaper
RegionList = ["en-US", "ja-JP", "en-IN", "pt-BR", "fr-FR", "de-DE", "en-CA", "en-GB", "it-IT", "es-ES", "fr-CA"] #add your country here

# Converts region codes to zoneinfo-supported time zone formats
def region_to_zone(region):
    # Split the region code, get the language code and country code
    language, country = region.split("-")
    # Return the corresponding time zone based on the country code
    if country == "US":
        return "America/New_York" # United States
    elif country == "JP":
        return "Asia/Tokyo" # Japan
    elif country == "IN":
        return "Asia/Kolkata" # India
    elif country == "BR":
        return "America/Sao_Paulo" # Brazil
    elif country == "FR":
        return "Europe/Paris" # France
    elif country == "DE":
        return "Europe/Berlin" # Germany
    elif country == "CA":
        return "America/Toronto" # Canada
    elif country == "GB":
        return "Europe/London" # United Kingdom
    elif country == "IT":
        return "Europe/Rome" # Italy
    elif country == "ES":
        return "Europe/Madrid" # Spain
    else:
        return None

#Create Readme.md for github display
info_path = os.path.join("global","README.md")
os.makedirs(os.path.dirname(info_path), exist_ok=True)
with open(info_path, "w", encoding='utf-8') as f:
    f.write(f"## Today's Bing Wallpaper\n")
    f.write(f"|      |      |      |\n")
    f.write(f"| :----: | :----: | :----: |\n")

#Main function
for region in RegionList:
    log_current_time = get_current_time()
    # Convert the region code to a time zone
    zone = region_to_zone(region)
    # If the time zone is not empty, use the zoneinfo module to get the local time
    if zone:
        tz = zoneinfo.ZoneInfo(zone)
        now = datetime.now()
        local_time = now.astimezone(tz)
    else:
        # If the time zone is empty, print the region code and an error message
        local_time = (f"{region}: Invalid region code")
        
    print(f"[{log_current_time}] Start geting global Bing Wallpaper, region={region}, local time is {local_time}")
    
    api_url_global = f"https://global.bing.com/HPImageArchive.aspx?n=1&setmkt={region}&setlang=en&idx=0&format=js"
    response = requests.get(api_url_global)
    if response.status_code == 200: #Check response
        data = response.json()
        urlbase = data["images"][0]["urlbase"]
        url = "https://www.bing.com" + urlbase + "_UHD.jpg"
        log_current_time = get_current_time()
        print(f"[{log_current_time}] Successful get url: {url}")
        image_data = requests.get(url).content

        #Note: The following code is used for wallpaper download. If you need it, just enable it.

        #image_path = os.path.join("global",region,"img","background.jpg")
        #os.makedirs(os.path.dirname(image_path), exist_ok=True)
        #with open(image_path, "wb") as f:
            #f.write(image_data)
            #f.close()
        #log_current_time = get_current_time()
        #print(f"[{log_current_time}] Picture saved to {image_path}")

        #End

        #All codes below is to write README.md to display on github.
        enddate = data["images"][0]["enddate"]
        yy = f"{enddate[:4]}"
        mm = f"{enddate[4:6]}"
        dd = f"{enddate[6:]}"
        enddate = f"{enddate[:4]}-{enddate[4:6]}-{enddate[6:]}"

        copy = data["images"][0]["copyright"]
        title = data["images"][0]["title"]
        info_path = os.path.join("global",region,"README.md")
        os.makedirs(os.path.dirname(info_path), exist_ok=True)
        with open(info_path, "w", encoding='utf-8') as f:
            f.write(f"## Today's Bing Wallpaper\n")
            f.write(f"Update: {enddate}\n")
            f.write(f"![]({url}&w=1000)Download: [{copy}]({url})")
            f.write(f"\n\nAuto get programm by LtgX\n")
        log_current_time = get_current_time()
        print(f"[{log_current_time}] Picture infomations saved to  {info_path}")

        history_file_name = f"{dd}_{region}.md"
        history_path = os.path.join("global",region,"history",yy,mm,history_file_name)
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        with open(history_path, "w", encoding='utf-8') as f:
            f.write(f"## History Bing Wallpaper\n")
            f.write(f"Wallpaper date: {enddate}\n")
            f.write(f"![]({url}&w=1000)Download: [{copy}]({url})")
            f.write(f"\n\nAuto get programm by LtgX\n")
        log_current_time = get_current_time()
        print(f"[{log_current_time}] Picture infomations saved to {history_path}")

        info_path = os.path.join("global","README.md")
        with open(info_path, "a", encoding='utf-8') as f:
            f.write(f"|{enddate}|**Region: {region}**||\n")
            f.write(f"||![]({url}&pid=hp&w=1152&h=648&rs=1&c=4)| [download]({url})|\n")
            f.write(f"||*Copyright: {copy}*\n||")
            f.write(f"\n|||\n")


    
    else:
        log_current_time = get_current_time()
        print(f"[{log_current_time}] Failed with statue code: {response.status_code}")

#By LtgX
info_path = os.path.join("global","README.md")
os.makedirs(os.path.dirname(info_path), exist_ok=True)
with open(info_path, "a", encoding='utf-8') as f:
    f.write(f"\nAuto get programm by LtgX\n")

log_current_time = get_current_time()
print(f"Program exit at {log_current_time}")
