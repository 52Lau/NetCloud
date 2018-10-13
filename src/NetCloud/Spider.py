# -*- coding: UTF-8 -*-
from NetCloud.NetCloudCrawler import NetCloudCrawl
from NetCloud.NetCloudAnalyse import NetCloudAnalyse


if __name__ == '__main__':
    song_name = "回首仍是少年"
    song_id = 1311345294
    singer_name = "张国荣"
    singer_id = 6457
    crawler = NetCloudCrawl(song_name,song_id,singer_name,singer_id)
    # 将歌手的全部热门评论存入文件
    #crawler.save_singer_all_hot_comments_to_file()

    # 获取一首歌的热门评论
    comments_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{song_id}/?csrf_token=".format(song_id=song_id)
    # hot_comments_list=crawler.get_hot_comments(comments_url)
    # for hot_comment in hot_comments_list:
    #     print(hot_comment)

    # all_comments_list=crawler.get_all_commentsBylau(comments_url)
    # for all_comment in all_comments_list:
    #     print(all_comment)

    # save_all_comments_list_Page=crawler.save_pages_commentsByLau(comments_url,1,10)
    # for comment in save_all_comments_list_Page:
    #     print(comment)
    crawler.threading_save_all_comments_to_fileByLau(comments_url,1,10,0.35)
    # crawler.generate_all_necessary_files(threads=10)
    #analyse = NetCloudAnalyse(song_name,singer_name,song_id,singer_id)
    # analyse.generate_all_analyse_files(threads=20)
    #绘制评论关键词的词云,full_comments = True 表示绘制 全部评论，False 表示绘制热门评论
    #analyse.draw_wordcloud(full_comments = False)