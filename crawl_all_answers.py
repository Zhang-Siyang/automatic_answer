#!/usr/bin/python
#-*- coding:utf-8 -*-
# Author:shi cheng
import json
import urllib2
import urllib
import requests
import os
import time
import random
import hashlib

# 请求地址
root_url = "http://xxjs.dtdjzx.gov.cn/quiz-api/"
getGameSubject_url = "game_info/getGameSubject"
lookBackSubject_url = "game_info/lookBackSubject"
def getGameSubject(user):
    # 请求地址
    url = root_url + getGameSubject_url
    # 请求参数
    requestData = {}
    # 转换对应格式
    params = json.dumps(requestData)
    # 请求头
    request = urllib2.Request(url, params)
    request.add_header('Content-Type', 'application/json; charset=utf-8')
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0")
    request.add_header("system-type", "web")
    request.add_header("user_hash", user)
    response = urllib2.urlopen(request)
    if response is not None:
        json_string = response.read()
    all_data = json.loads(json_string)
    # 数据整理
    msg = all_data['msg']
    code = all_data['code']
    print '抽取新题目：', msg, "code:", code
    if (int(code) == 200):
        recordId = all_data['data']['recordId']
        roundOnlyId = all_data['data']['roundOnlyId']
        subjectInfoList = all_data['data']['subjectInfoList']
        return subjectInfoList, roundOnlyId
    else:
        return None, None
def lookBackSubject(roundOnlyId):
    data = {"roundOnlyId": roundOnlyId}
    req = requests.post(root_url + lookBackSubject_url, data=data)
    ans_data = req.json()
    print '获取对应答案：',ans_data['msg']
    return ans_data['data']['dateList']
def save_txt(txtString,txtFile):
    with open(txtFile, 'w') as f:
        txtString = 'var ans = '+ txtString + ';'
        f.write(txtString)
        f.close()
def read_txt(txtFile):
    if os.path.exists(txtFile):
        f = open(txtFile)
        txtString = f.read()
        txtString = txtString.replace('var ans =', '').replace(';', '')
        f.close()
        return txtString
    else:
        return None
# 使用python自带的hashlib库
def get_md5_value(str):
    my_md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
    my_md5.update(str)  # 得到MD5消息摘要
    my_md5_Digest = my_md5.hexdigest()  # 以16进制返回消息摘要，32位
    return my_md5_Digest
def check_md5():
    old_MD5 = '93258a2225bc4c9650eab620a9998c4a'
    js_URL ='http://xxjs.dtdjzx.gov.cn/js/kaiShiJingSai/kaishijingsai.js'
    urllib.urlretrieve(js_URL, 'new.js')
    f = open('new.js','r')
    new_MD5 = get_md5_value(f.read())
    f.close()
    if  new_MD5 == old_MD5:
        print 'MD5检测正常！'
        os.remove('new.js')
        return True
    else:
        print '检测到变化!!!  新版MD5：',new_MD5
        return False

if __name__ == '__main__':
    # 先判断网站反作弊手段是否变化
    if check_md5():
        user = '13567897654'
        # 保存答案的字典
        ans_base_dist = {}
        # 答案的保存路径
        txt_path = 'all_answer_set.txt'
        # 获取之前保存的题目
        txtString = read_txt(txt_path)
        if txtString :
            ans_base_dist = json.loads(txtString)
            print "发现之前保存答案，长度：",len(ans_base_dist)
        else:
            print "未发现之前保存答案！"
        #开始获取网络题目
        for i in range(30):
            #每次获取20道题目
            print "第",i+1,'次获取新答案！'
            subjectInfoList , roundOnlyId = getGameSubject(user)
            if(roundOnlyId):
                #获取答案
                dateList= lookBackSubject(roundOnlyId)
                for j in range(20):
                    for k in range(20):
                        qid = subjectInfoList[j]['id']
                        aid = dateList[k]['subjectId']
                        answer = dateList[k]['answer']
                        if (qid == aid):
                            if ans_base_dist.has_key(qid):
                                if ans_base_dist[qid]!=answer:
                                    print "发现不同答案!"
                            else:
                                ans_base_dist[qid] = answer
                                print "添加新答案!，目前长度：",len(ans_base_dist)
                                txtString = json.dumps(ans_base_dist)
                                save_txt(txtString, txt_path)
            else:
                print "获取试题失败！"
            time.sleep(5)
        print "新版答案库长度：",len(ans_base_dist)
        print txtString

