#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time   : 2018/1/26
# @Author : Lyrichu
# @Email  : 919987476@qq.com
# @File   : NetCloudCrawler
'''
@Description:
Netease Cloud Music comments spider,you can use it to crawl all comments of 
a song,and also you can crawl the users info. WIth all this content,you can
do some interesting analyse like view the keywords of comments,the location distribution
of commenters,the age distribution etc. The class NetCloudCrawler does the job of crawler
comments,and the other class NetCloudAnalyse does the job of analyse of comments and users'
info. 
reference:@平胸小仙女's article(address:https://www.zhihu.com/question/36081767)
post encryption part can be found in the following articles:
author：平胸小仙女
link：https://www.zhihu.com/question/36081767/answer/140287795
source：知乎
-----------------------
version2,add multithreading crawler,add supporting to python3.x
'''
from Crypto.Cipher import AES
import base64
import requests
import json
import time
import os
import re 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from threading import Thread

from src.NetCloud import HttpPost


class NetCloudCrawl(object):
    '''
    the main crawler class
    '''
    def __init__(self,song_name,song_id,singer_name,singer_id):
        self.song_name = song_name
        self.song_id = song_id
        self.singer_name = singer_name
        self.singer_id = singer_id
        self.comments_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{song_id}/?csrf_token=".format(song_id = song_id)
        self.singer_url = 'http://music.163.com/artist?id={singer_id}'.format(singer_id = singer_id)
        # save all songs file to directory songs_root_dir
        self.songs_root_dir = "songs"
        if not os.path.exists(self.songs_root_dir):
            os.mkdir(self.songs_root_dir)
        self.singer_path = os.path.join(self.songs_root_dir,self.singer_name)
        if not os.path.exists(self.singer_path):
            os.mkdir(self.singer_path)
        self.song_path = os.path.join(self.singer_path,self.song_name)
        if not os.path.exists(self.song_path):
            os.mkdir(self.song_path)
        # where to save crawled comments file
        self.comments_file_path = os.path.join(self.song_path,self.song_name+".csv")
        # comment users info file path
        self.users_info_file_path = os.path.join(self.song_path,"users_info.csv")
        # headers info
        self.headers = {
        'Host':"music.163.com",
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept-Encoding':"gzip, deflate",
        'Content-Type':"application/x-www-form-urlencoded",
        'Cookie':"_ntes_nnid=754361b04b121e078dee797cdb30e0fd,1486026808627; _ntes_nuid=754361b04b121e078dee797cdb30e0fd; JSESSIONID-WYYY=yfqt9ofhY%5CIYNkXW71TqY5OtSZyjE%2FoswGgtl4dMv3Oa7%5CQ50T%2FVaee%2FMSsCifHE0TGtRMYhSPpr20i%5CRO%2BO%2B9pbbJnrUvGzkibhNqw3Tlgn%5Coil%2FrW7zFZZWSA3K9gD77MPSVH6fnv5hIT8ms70MNB3CxK5r3ecj3tFMlWFbFOZmGw%5C%3A1490677541180; _iuqxldmzr_=32; vjuids=c8ca7976.15a029d006a.0.51373751e63af8; vjlast=1486102528.1490172479.21; __gads=ID=a9eed5e3cae4d252:T=1486102537:S=ALNI_Mb5XX2vlkjsiU5cIy91-ToUDoFxIw; vinfo_n_f_l_n3=411a2def7f75a62e.1.1.1486349441669.1486349607905.1490173828142; P_INFO=m15527594439@163.com|1489375076|1|study|00&99|null&null&null#hub&420100#10#0#0|155439&1|study_client|15527594439@163.com; NTES_CMT_USER_INFO=84794134%7Cm155****4439%7Chttps%3A%2F%2Fsimg.ws.126.net%2Fe%2Fimg5.cache.netease.com%2Ftie%2Fimages%2Fyun%2Fphoto_default_62.png.39x39.100.jpg%7Cfalse%7CbTE1NTI3NTk0NDM5QDE2My5jb20%3D; usertrack=c+5+hljHgU0T1FDmA66MAg==; Province=027; City=027; _ga=GA1.2.1549851014.1489469781; __utma=94650624.1549851014.1489469781.1490664577.1490672820.8; __utmc=94650624; __utmz=94650624.1490661822.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; playerid=81568911; __utmb=94650624.23.10.1490672820",
        'Connection':"keep-alive",
        'Referer':'http://music.163.com/',
        'Upgrade-Insecure-Requests':"1"
        }
        # set the proxies
        self.proxies= {
            'http:':'http://122.114.31.177',
            'https:':'https://39.86.40.74'
        }
        # value of offset is:(comment_page-1)*20,if it's the first page,total is True,else False
        # first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}' # first parameter
        self.second_param = "010001" # 第二个参数
        # the third parameter
        self.third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        # the fourth parameter
        self.forth_param = "0CoJUm6Qyw8W8jud"
        self.encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"

        
    def get_params(self,page): 
        '''
        get the necesarry parameters
        :param page: the input page
        '''
        first_key = self.forth_param
        second_key = 16 * 'F'
        iv = "0102030405060708"
        if(page == 1): # if it's the first page
            first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
            h_encText = self.AES_encrypt(first_param, first_key,iv)
        else:
            offset = str((page-1)*20)
            first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
            h_encText = self.AES_encrypt(first_param, first_key, iv)
        h_encText = self.AES_encrypt(h_encText, second_key, iv)
        return h_encText

    
    def AES_encrypt(self,text, key, iv):
        '''
        the function of deciphering
        '''
        pad = 16 - len(text) % 16
        if isinstance(text,bytes): # convert text to str
            text = text.decode("utf-8")
        text += pad*chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    
    def get_json(self,url,params, encSecKey):
        '''
        get the comments json data
        '''
        data = {
             "params": params,
             "encSecKey": encSecKey
        }
        response = requests.post(url, headers=self.headers, data=data,proxies = self.proxies)
        return response.content

    
    def get_hot_comments(self,url,real):
        '''
        get the hot comments list
        :param url:the crawl url
        :return:the hot comments list
        '''
        hot_comments_list = []
        params = self.get_params(1) # the first page
        json_text = self.get_json(url,params,self.encSecKey)
        if isinstance(json_text,bytes):
            json_text = json_text.decode("utf-8") # convert json_text from bytes to str
        json_dict = json.loads(json_text)
        try:
            hot_comments = json_dict['hotComments'] # hot comments
            print("There are %d hot comments!" % len(hot_comments))
            for item in hot_comments:
                    comment = item['content'] # comments content
                    # replace comma to blank,because we want save text as csv format,
                    # which is seperated by comma,so the commas in the text might cause confusions
                    comment = comment.replace(","," ").replace("\n"," ")
                    likedCount = item['likedCount'] # the total agreements num
                    comment_time = item['time'] # comment time(formatted in timestamp)
                    userID = item['user']['userId'] # the commenter id
                    nickname = item['user']['nickname'] # the nickname
                    nickname = nickname.replace(","," ")
                    avatarUrl = item['user']['avatarUrl'] 
                    # the comment info string
                    comment_info = "{userID},{nickname},{avatarUrl},{comment_time},{likedCount},{comment}\n".format(
                        userID = userID,nickname = nickname,avatarUrl = avatarUrl,comment_time = comment_time,
                        likedCount = likedCount,comment = comment
                        )
                    # 对评论内容进行情感分析 积极、消极情绪绝对值大于0.45
                    responseText = json.loads(self.SendHttpPost(comment))
                    positive_prob = responseText['items'][0]['positive_prob']
                    negative_prob = responseText['items'][0]['negative_prob']
                    a = abs(positive_prob - negative_prob)
                    if (a > real):
                        path = self.song_path + '\\' + avatarUrl.split("/")[-1]
                        # 转换成localtime
                        time_local = time.localtime(comment_time)
                        # 转换成新的时间格式(2016-05-05 20:28:54)
                        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                        info = "@" + nickname + "\n\n" + dt + "\n\n在《" + self.song_name + "》下的评论"
                        self.PictureSpider(avatarUrl, path, info, comment)
                        hot_comments_list.append(comment_info)
        except KeyError as key_error:
            print("Server parse error:{error}".format(error = key_error))
        except Exception as e:
            print("Fail to get all hot comments:{error}".format(error = e))
        finally:
            print("Get hot comments done!")
        return hot_comments_list

    #发送HTTP POST请求
    def SendHttpPost(self,text):
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.d2b76c265c2b62ab92e589059e86d830.2592000.1540781521.282335-11600751&charset=UTF-8'
        body = {"text": text}
        headers = {'content-type': "application/json"}
        # print type(body)
        # print type(json.dumps(body))
        # 这里有个细节，如果body需要json形式的话，需要做处理
        # 可以是data = json.dumps(body)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        # 也可以直接将data字段换成json字段，2.4.3版本之后支持
        # response  = requests.post(url, json = body, headers = headers)

        # 返回信息
        #print(response.text)
        # 返回响应头
        #print(response.status_code)
        return response.text

    def  PictureSpider(self,url,path,info,text):
        '''
        下载评论者用户头像
        '''
        try:
            if not os.path.exists(path):
                r = requests.get(url)
                r.raise_for_status()
                # 使用with语句可以不用自己手动关闭已经打开的文件流
                with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(r.content)
                #合成图片
                self.PictureCut(info,path,text)
                print("爬取完成")
            else:
                print("文件已存在")
        except Exception as e:
            print("爬取失败:" + str(e))

    def PictureCut(self,info,Path,text):

        #需要处理的图片路径 输覆盖原文件

        # 设置所使用的字体
        font = ImageFont.truetype("src/NetCloud/source/simsun.ttc", 30)
        font2 = ImageFont.truetype("src/NetCloud/source/simsun.ttc", 45)
        # 加载底图
        base_img = Image.open(u'D:\PyCharm\\NetCloud\\src\\NetCloud\songs\张国荣\\bg.jpg')
        # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
        # print base_img.size, base_img.mode
        box = (20, 320, 270, 590)  # 底图上需要P掉的区域  x轴 y轴 宽（减去x） 高（减去y）

        # 加载需要P上去的图片
        tmp_img = Image.open(u''+Path)
        # 这里可以选择一块区域或者整张图片
        # region = tmp_img.crop((0,0,304,546)) #选择一块区域
        # 或者使用整张图片
        region = tmp_img

        # 使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
        # 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
        # 提前将图片进行缩放，以适应box区域大小
        # region = region.rotate(180) #对图片进行旋转
        region = region.resize((box[2] - box[0], box[3] - box[1]))
        base_img.paste(region, box)

        # 画图
        draw = ImageDraw.Draw(base_img)
        # 评论者信息
        draw.text((300, 400), info, (255, 0, 0),font=font)  # 设置文字位置/内容/颜色/字体
        # 评论内容
        #text = '目前唯一支撑我活下去的就是我的父母了，想要让父母过得更好，不想结婚也不想交男朋友，深夜时总会一个人躺在床上胡思乱想，父母已经不年轻了，总有一天会先于我离开，真的到了那一天……我不知道我会不会跟着一起走，只希望，他们可以长命百岁，虽然不太可能，但是我自私的希望他们可以过得比我更久'
        textPur = ''
        while text:
            textPur = textPur + text[:18] + "\n"
            # print(text[:20])
            text = text[18:]
        draw.text((32, 630), textPur, (255, 0, 0), font=font2)  # 设置文字位置/内容/颜色/字体
        draw = ImageDraw.Draw(base_img)

        #base_img.show()  # 查看合成的图片
        #base_img.save('./out.png')  # 保存图片
        base_img.save(Path)  # 保存图片

    def get_all_comments(self):
        '''
        get a song's all comments in order,note
        that if the comments num is big,this will cost maybe a long time,
        you can use the function threading_save_all_comments_to_file() to speed the crawling. 
        but this will ensure the comments we crawled is in order,but the multi threaidng crawling 
        will not. 
        '''
        all_comments_list = [] # put all comments here
        all_comments_list.append("用户ID,用户昵称,用户头像地址,评论时间,点赞总数,评论内容\n") # headers
        params = self.get_params(1)
        json_text = self.get_json(self.comments_url,params,self.encSecKey)
        if isinstance(json_text,bytes):
            json_text = json_text.decode("utf-8") # convert json_text from bytes to str
        json_dict = json.loads(json_text)
        comments_num = int(json_dict['total'])
        if(comments_num % 20 == 0):
            page = comments_num // 20
        else:
            page = int(comments_num / 20) + 1
        print("Song name:{song_name}".format(song_name = self.song_name))
        print("There are %d pages of comments!" % page)
        for i in range(page):  # crawl in pages' order
            params = self.get_params(i+1)
            json_text = self.get_json(self.comments_url,params,self.encSecKey)
            if isinstance(json_text,bytes):
                json_text = json_text.decode("utf-8") # convert json_text from bytes to str
            json_dict = json.loads(json_text)
            if i == 0:
                print("There are total %d comments!" % comments_num) # all comments count
            try:
                for item in json_dict['comments']:
                    comment = item['content'] # the comments content
                    # replace comma to blank,because we want save text as csv format,
                    # which is seperated by comma,so the commas in the text might cause confusions
                    comment = comment.replace(","," ")
                    likedCount = item['likedCount'] 
                    comment_time = item['time'] 
                    userID = item['user']['userId'] 
                    nickname = item['user']['nickname'] 
                    avatarUrl = item['user']['avatarUrl'] 
                    comment_info = "{userID},{nickname},{avatarUrl},{comment_time},{likedCount},{comment}\n".format(
                        userID = userID,nickname = nickname,avatarUrl = avatarUrl,comment_time = comment_time,
                        likedCount = likedCount,comment = comment
                        )
                    all_comments_list.append(comment_info)
            except KeyError as key_error:
                print("Fail to get page {page}.".format(page = i+1))
                print("Server parse error:{error}".format(error = key_error))
            except Exception as e:
                print("Fail to get page {page}.".format(page = i+1))
                print(e)
            else:
                print("Successfully to get page {page}.".format(page = i+1))
        return all_comments_list

    def threading_save_all_comments_to_fileByLau(self,comments_url,beginPage,endPage,real,threads = 1):
        '''
        use multi threading to get all comments,note that will not
        ensure the crawled comments' order
        :param threads: the threads num we use
        '''
        start_time = time.time()
        with open(self.comments_file_path,"w",encoding = "utf-8") as fout:
            fout.write("用户ID,用户昵称,用户头像地址,评论时间,点赞总数,评论内容\n") # headers
        params = self.get_params(1)
        json_text = self.get_json(comments_url,params,self.encSecKey)
        if isinstance(json_text,bytes):
            json_text = json_text.decode("utf-8") # convert json_text from bytes to str
        json_dict = json.loads(json_text)
        comments_num = int(json_dict['total'])
        if(comments_num % 20 == 0):
            page = comments_num // 20
        else:
            page = int(comments_num / 20) + 1
        print("Song name:{song_name}".format(song_name = self.song_name))
        print("There are %d pages of total %d comments!" % (page,comments_num))
        pack = page//threads
        threads_list = []
        for i in range(threads):
            begin_page = i*pack
            if i < threads-1:
                end_page = (i+1)*pack
            else:
                end_page = page
            t = Thread(target = self.save_pages_commentsByLau,args = (comments_url,beginPage,endPage,real))
            threads_list.append(t)
        for i in range(threads):
            threads_list[i].start()
        for i in range(threads):
            threads_list[i].join()
        end_time = time.time()
        print("Using {threads} threads,it costs {cost_time} seconds to crawl <{song_name}>'s all comments!"
                .format(threads = threads,cost_time = (end_time - start_time),song_name = self.song_name))



    def save_pages_commentsByLau(self,url,begin_page,end_page,real):
        '''
        单独调用某个模块
        save comments page between begin_page and end_page
        :param begin_page: the begin page
        :param end_page: the end page
        '''
        comment_info_list = []
        with open(self.comments_file_path,"a",encoding = "utf-8") as fout:
            for i in range(begin_page,end_page):
                params = self.get_params(i+1)
                json_text = self.get_json(url,params,self.encSecKey)
                if isinstance(json_text,bytes):
                    json_text = json_text.decode("utf-8") # convert json_text from bytes to str
                json_dict = json.loads(json_text)
                try:
                    for item in json_dict['comments']:
                        comment = item['content']
                        # replace comma to blank,because we want save text as csv format,
                        # which is seperated by comma,so the commas in the text might cause confusions
                        comment = comment.replace(","," ")
                        likedCount = item['likedCount']
                        comment_time = item['time']
                        userID = item['user']['userId']
                        nickname = item['user']['nickname']
                        nickname = nickname.replace(","," ")
                        avatarUrl = item['user']['avatarUrl']

                        # the comment info string
                        comment_info = "{userID},{nickname},{avatarUrl},{comment_time},{likedCount},{comment}\n".format(
                            userID = userID,nickname = nickname,avatarUrl = avatarUrl,comment_time = comment_time,
                            likedCount = likedCount,comment = comment
                            )
                        # 对评论内容进行情感分析 积极、消极情绪绝对值大于0.45
                        responseText = json.loads(HttpPost.SendHttpPost(comment))
                        positive_prob = responseText['items'][0]['positive_prob']
                        negative_prob = responseText['items'][0]['negative_prob']
                        a = abs(positive_prob - negative_prob)
                        if (a > real):
                            path = self.song_path + '\\' + avatarUrl.split("/")[-1]
                            # 转换成localtime
                            time_local = time.localtime(comment_time/1000)
                            # 转换成新的时间格式(2016-05-05 20:28:54)
                            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                            info = "@" + nickname + "\n\n" + dt + "\n\n在《" + self.song_name + "》下的评论"
                            self.PictureSpider(avatarUrl, path, info, comment)
                            comment_info_list.append(comment_info)
                except KeyError as key_error:
                    print("Fail to get page {page}.".format(page = i+1))
                    print("Server parse error:{error}".format(error = key_error))
                except Exception as e:
                    print("Fail to get page {page}.".format(page = i+1))
                    print(e)
                else:
                    print("Successfully to save page {page}.".format(page = i+1))
            #热门评论
            hot_comments=self.get_hot_comments(url,real)
            for comment in hot_comments:
                comment_info_list.append(comment)
            fout.writelines(comment_info_list)
            print("Write page {begin_page} to {end_page} successfully!".format(begin_page = begin_page,end_page = end_page))
            return comment_info_list
    
    def save_to_file(self,comments_list,filename):
        '''
        save comments to file
        '''
        with open(filename,"w",encoding='utf-8') as f:
            f.writelines(comments_list)
        print("Write to file {filename} successfully".format(filename = filename))

    # save all comments to csv file
    def save_all_comments_to_file(self):
        start_time = time.time() 
        all_comments_list = self.get_all_comments()
        self.save_to_file(all_comments_list,self.comments_file_path)
        end_time = time.time() 
        print("It costs %.2f seconds to crawler <%s>." % (end_time - start_time,self.song_name))

    def get_singer_hot_songs_ids(self,singer_url):
        '''
        get a singer's all hot songs ids list
        :param singer_url: the singer domain page url
        '''
        ids_list = []
        html = requests.get(singer_url,headers = self.headers,proxies = self.proxies).text
        pattern = re.compile(r'<a href="/song\?id=(\d+?)">.*?</a>')
        ids = re.findall(pattern,html)
        for id in ids:
            ids_list.append(id)
        return ids_list

    def get_lyrics(self):
    	'''
    	get music lyrics
    	:return: json format music lyrics
    	'''
    	lyrics_url = "http://music.163.com/api/song/lyric?os=pc&id={id}&lv=-1&kv=-1&tv=-1".format(id = self.song_id)
    	lyrics = requests.get(lyrics_url,headers = self.headers,proxies = self.proxies).text 
    	return lyrics

    def save_lyrics_to_file(self):
    	lyrics_json = json.loads(self.get_lyrics())
    	lyrics_str = lyrics_json['lrc']['lyric']
    	pattern = r'\[\d+:\d+\.\d+\](.+?\n)'
    	lyrics_list = re.findall(pattern,lyrics_str)
    	save_path = os.path.join(self.song_path,"{song_name}_lyrics.txt".format(song_name = self.song_name))
    	with open(save_path,"w",encoding = "utf-8") as f:
    		f.write("{song_name}\n{singer_name}\n".format(song_name = self.song_name,singer_name = self.singer_name))
    		f.writelines(lyrics_list)
    	print("save {save_path} successfully!".format(save_path = save_path))


    def save_singer_all_hot_comments_to_file(self):
        '''
        get a singer's all hot songs' hot comments
        :param singer_name: the name of singer
        :param singer_id:the id of singer
        '''
        song_ids = self.get_singer_hot_songs_ids(self.singer_url) # get all hot songs ids
        # first line is headers
        all_hot_comments_list = ["用户ID,用户昵称,用户头像地址,评论时间,点赞总数,评论内容\n"]
        for song_id in song_ids:
            url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{song_id}/?csrf_token=".format(song_id = song_id)
            hot_comments_list = self.get_hot_comments(url)
            all_hot_comments_list.extend(hot_comments_list)
        self.save_to_file(all_hot_comments_list,os.path.join(self.singer_path,"hot_comments.csv"))
        print("Write {singer_name}'s {num} hot songs hot comments successfully!".format(singer_name = self.singer_name,num = len(song_ids)))

    def generate_all_necessary_files(self,threads = 10):
        '''
        generate all necessary files,including:
        1. hot comments file
        2. full comments file
        '''
        self.threading_save_all_comments_to_file(threads)
        self.save_singer_all_hot_comments_to_file()


    def _test_save_singer_all_hot_comments_to_file(self):
        self.save_singer_all_hot_comments_to_file()

    def _test_get_singer_hot_songs_ids(self):
        print(self.get_singer_hot_songs_ids(self.singer_url))

    def _test_save_all_comments_to_file(self):
        self.save_all_comments_to_file()

    def _test_threading_save_all_comments_to_file(self):
        self.threading_save_all_comments_to_file()

    def _test_get_lyrics(self):
    	lyrics = self.get_lyrics()
    	print(lyrics)
    	print(type(lyrics))

    def _test_save_lyrics_to_file(self):
    	self.save_lyrics_to_file()

    def _test_netcloudcrawler_all(self):
        '''
        run all test functions
        '''
        self._test_get_singer_hot_songs_ids()
        self._test_save_all_comments_to_file()
        self._test_save_singer_all_hot_comments_to_file()
        self._test_threading_save_all_comments_to_file()





if __name__ == '__main__':
    song_name = '听海'
    song_id = 28314060
    singer_name = '周杰伦'
    singer_id = 6452
    comments_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{song_id}/?csrf_token=".format(
        song_id=song_id)
    netcloud_spider = NetCloudCrawl(song_name = song_name, song_id = song_id,
                                    singer_name = singer_name,singer_id = singer_id)
    #netcloud_spider._test_netcloudcrawler_all()
    #netcloud_spider.generate_all_necessary_files(100)
    #netcloud_spider._test_get_lyrics()
    netcloud_spider._test_save_lyrics_to_file()
    #netcloud_spider.threading_save_all_comments_to_fileByLau(comments_url, 1, 50, 0.45)
    comment_list=netcloud_spider.save_pages_commentsByLau(comments_url, 1, 50, 0.45)
    for comment in comment_list:
        print(comment)




