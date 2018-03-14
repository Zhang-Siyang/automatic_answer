#!/usr/bin/python
#-*- coding:utf-8 -*-
# Author:shi cheng
import json
import urllib2
import requests
import os
import time


# 请求地址
root_url = "http://xxjs.dtdjzx.gov.cn/quiz-api/"
getGameSubject_url = "game_info/getGameSubject"
lookBackSubject_url = "game_info/lookBackSubject"

def getGameSubject(user = "17777777777"):
    # 请求地址
    url = root_url + getGameSubject_url
    # 请求参数
    requestData ={ }
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
    #数据整理
    msg=all_data['msg']
    code=all_data['code']
    recordId= all_data['data']['recordId']
    roundOnlyId = all_data['data']['roundOnlyId']
    subjectInfoList = all_data['data']['subjectInfoList']
    print '抽取20道题目：',msg
    return subjectInfoList,roundOnlyId

    # # 第一题
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]['id']
    # # 第一题选项一
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]['optionInfoList'][0]
    # # 第一题     选项一id
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]['optionInfoList'][0]['id']
    # # 第一题     选项一内容
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]['optionInfoList'][0]['optionTitle']
    # # 第一题     选项一 位置：ABCD
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]['optionInfoList'][0]['optionType']
    #
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]['optionInfoList'][1]
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]['optionInfoList'][2]
    # print  'subjectInfoList: ', all_data['data']['subjectInfoList'][0]['optionInfoList'][3]

def lookBackSubject(roundOnlyId):
    data = {"roundOnlyId": roundOnlyId}
    req = requests.post(root_url + lookBackSubject_url, data=data)
    ans_data = req.json()
    print '获取对应答案：',ans_data['msg']
    # print ans_data['code']
    # print ans_data['data']
    # print ans_data['data']['dateList']
    # 数据整理
    # msg = all_data['msg']
    # code = all_data['code']
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
if __name__ == '__main__':
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
    for i in range(50):
        #每次获取20道题目
        user = "17777777777"
        subjectInfoList , roundOnlyId = getGameSubject(user)
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
        time.sleep(10)
    print "新版答案库长度：",len(ans_base_dist)
    txtString = json.dumps(ans_base_dist)
    save_txt(txtString, txt_path)
    print txtString
