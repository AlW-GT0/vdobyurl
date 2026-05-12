import os
from getVdolist import getVdolist_1
from makeup import makeup

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
# 一般情况下设置为7000-8000即可
# 参考命令 nohup python -u make.py > ./1.log &
if __name__ == "__main__":
    output_dir='./vdoutput/AIF/ZhangYY/'
    domain = "https://bd.yfp1.pro:8869/" 
    url1 = '/result.html?key=%E5%BC%A0%E5%85%83%E8%8B%B1&page=' # "/index/search/?keyword=xx&page=" #
    # url1 = '/cate.html?cid=4&subcid=23&page='
    url2 = "" # "&limit=30" #
    make(domain, url1, url2, 1, 1, output_dir)
    # url = '/index/search/?keyword=&page=76&limit=30'
    # getVdolist_1(domain, url, output_dir)