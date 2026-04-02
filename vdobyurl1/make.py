import os
from dloadVdo import dloadM3u8
from getVdolist import getVdolist_1

def makeup(makeuplist):
    for path in makeuplist:
        p4l = f'{path}/mulist.txt'
        mulist = []
        with open(p4l, 'r') as f:
            for line in f:
                url = line.strip() # 去除每行首尾空白字符（及换行符）
                if url: # 跳过空行
                    mulist.append(url)
        odir = path
        dloadM3u8(mulist, odir)

def make(domain, url1, url2, start, amount, output_dir):
    makeuplist = []
    for i in range(amount):
        url = f'{url1}{start+i}{url2}'
        opath = f'{output_dir}/{start+i}/'
        makeuplist.append(opath)
        getVdolist_1(domain, url, opath)
    makeup(makeuplist)

# 在获取特殊类型时，
# 有必要将timeout切换到11000（s）
# 一般情况下设置为7000-8000即可 https://.pro:8869/result.html?key=%E8%B0%xx
# 参考命令 nohup python -u make.py > ./1.log &
if __name__ == "__main__":
    output_dir='./vdoutput/XP/tiaojiao/'
    domain = "https:/.pro:8869/"#"https://.cc:8888/" # "https://.pro:6788/" #
    url1 = '/result.html?key=%E8%B0%xx&page=' # "/index/search/?keyword=xx&page=" #
    # url1 = '/cate.html?cid=4&subcid=23&page='
    url2 = "" # "&limit=30" #
    make(domain, url1, url2, 9, 1, output_dir)
    # url = '/index/search/?keyword=&page=76&limit=30'
    # getVdolist_1(domain, url, output_dir)
    # https://.pro:8869/video.html?vid=111604