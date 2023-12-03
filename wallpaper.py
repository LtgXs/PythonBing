# 导入 requests 库，用于发送 HTTP 请求
import requests
# 导入 os 库，用于操作文件和目录
import os

# 定义 API 的地址
api_url = "https://www.bing.com/HPImageArchive.aspx?n=1&mkt=zh-cn&idx=0&format=js"
# 发送 GET 请求，获取响应
response = requests.get(api_url)
# 判断响应是否成功
if response.status_code == 200:
    # 解析响应的 json 数据
    data = response.json()
    # 从 json 数据中读取 urlbase 项
    urlbase = data["images"][0]["urlbase"]
    # 定义一个变量 url，变量值为 www.bing.com 加 urlbase 项的值加 _UHD.jpg
    url = "https://www.bing.com" + urlbase + "_UHD.jpg"
    # 发送 GET 请求，获取图片的二进制数据
    image_data = requests.get(url).content
    # 定义图片的保存路径，如果 img 文件夹不存在，就创建它
    image_path = os.path.join("img", "background.jpg")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    # 以二进制写入模式打开图片文件，写入图片数据，关闭文件
    with open(image_path, "wb") as f:
        f.write(image_data)
        f.close()
    # 打印成功的信息
    print(f"图片已经保存到 {image_path}")


    # 从 json 数据中读取 enddate 项，格式化为 yyyy-mm-dd 的形式
    enddate = data["images"][0]["enddate"]
    enddate = f"{enddate[:4]}-{enddate[4:6]}-{enddate[6:]}"
    # 从 json 数据中读取 copyright 项
    copy = data["images"][0]["copyright"]
    # 从 json 数据中读取 title 项
    title = data["images"][0]["title"]
    # 定义 info.txt 的保存路径，如果 img 文件夹不存在，就创建它
    info_path = os.path.join("img", "info.txt")
    os.makedirs(os.path.dirname(info_path), exist_ok=True)
    # 以文本写入模式打开 info.txt 文件，写入 enddate, copy, title 的内容，关闭文件
    with open(info_path, "w", encoding='utf-8') as f:
        f.write(f"Picture Title: {title}\n")
        f.write(f"Copyright: {copy}\n")
        f.write(f"Update: {enddate}\n")
        f.write(f"\nFrom Bing API\n")
        f.write(f"\nAuto get programm by LtgX\n")        
        f.close()
        
    # 打印成功的信息
    print(f"信息已经保存到 {info_path}")
else:
    # 打印失败的信息
    print(f"请求失败，状态码为 {response.status_code}")
