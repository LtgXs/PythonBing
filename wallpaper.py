import requests
import os


api_url = "https://www.bing.com/HPImageArchive.aspx?n=1&mkt=zh-cn&idx=0&format=js"
response = requests.get(api_url)
if response.status_code == 200:
    
    data = response.json()
    urlbase = data["images"][0]["urlbase"]
    url = "https://www.bing.com" + urlbase + "_UHD.jpg"
    image_data = requests.get(url).content
    image_path = os.path.join("img", "background.jpg")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(image_data)
        f.close()
    print(f"图片已经保存到 {image_path}")

    enddate = data["images"][0]["enddate"]
    yy = f"{enddate[:4]}"
    mm = f"{enddate[4:6]}"
    dd = f"{enddate[6:]}"
    enddate = f"{enddate[:4]}-{enddate[4:6]}-{enddate[6:]}"

    copy = data["images"][0]["copyright"]
    title = data["images"][0]["title"]
    info_path = os.path.join("README.md")
    with open(info_path, "w", encoding='utf-8') as f:
        f.write(f"## Today's Bing Wallpaper\n")
        f.write(f"Update: {enddate}\n")
        f.write(f"![]({url}&w=1000)Download: [{copy}]({url})")
        f.write(f"\n\nAuto get programm by LtgX\n")
    print(f"信息已经保存到 {info_path}")

    history_file_name = f"{dd}.md"
    history_path = os.path.join("history",yy,mm,history_file_name)
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding='utf-8') as f:
        f.write(f"## History Bing Wallpaper\n")
        f.write(f"Wallpaper date: {enddate}\n")
        f.write(f"![]({url}&w=1000)Download: [{copy}]({url})")
        f.write(f"\n\nAuto get programm by LtgX\n")
    print(f"信息已经保存到 {history_path}")
    
else:
    print(f"请求失败，状态码为 {response.status_code}")
