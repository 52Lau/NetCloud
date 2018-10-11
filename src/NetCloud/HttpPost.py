#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def SendHttpPost(text):
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

def HttpGet():
    r = requests.get(url='http://123.207.35.36:5010/get/')
    print(r.text)  # 查看请求返回的状态
    # 结果


if __name__ == '__main__':
    # comment=SendHttpPost('去年差不多也是这个时候听到这首歌  觉得就是为自己而写的  现在依然这样觉得  只不过  那个让我觉得温暖的人  不再是他')
    # responseText = json.loads(comment)
    # positive_prob = responseText['items'][0]['positive_prob']
    # negative_prob = responseText['items'][0]['negative_prob']
    # a=abs(positive_prob-negative_prob)
    # if (a>0.45):
    #     print('gt')
    for i in range(1,100):
        HttpGet()
