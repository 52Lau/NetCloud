import requests
import os
url = "http://p2.music.126.net/S8RMY7OzALENG3h9SxcaNg==/18919296579372684.jpg"
root = "D:\PyCharm\\NetCloud\\src\\NetCloud\songs\张国荣\敢爱\\"
path = root + url.split("/")[-1]

def  PictureSpider(url,path):
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url)
            r.raise_for_status()
            # 使用with语句可以不用自己手动关闭已经打开的文件流
            with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                f.write(r.content)
            print("爬取完成")
        else:
            print("文件已存在")
    except Exception as e:
        print("爬取失败:" + str(e))


if __name__ == '__main__':
    PictureSpider(url,path)