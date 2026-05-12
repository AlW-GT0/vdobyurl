import os
from threading import Thread

from getVdolist import getVdolist_4novel
from makeup import makeup


def makenovel(domain, output_dir):
    makeuplist = []
    opath = getVdolist_4novel(domain, output_dir)
    makeuplist.append(opath)
    makeup(makeuplist)

def makenovel2thread(domain, output_dir):
    opath = getVdolist_4novel(domain, output_dir)
    
    # 这一段将一个mulist的内容分布到两个子文件夹中
    mupath = f'{opath}/mulist.txt'
    opath1 = f'{opath}/1/'
    opath2 = f'{opath}/2/'
    os.makedirs(opath1, exist_ok=True)
    os.makedirs(opath2, exist_ok=True)
    mupath1 = f'{opath1}/mulist.txt'
    mupath2 = f'{opath2}/mulist.txt'
    mulist = []
    with open(mupath, "r") as f:
        for line in f:
            mulist.append(line)
    f1 = open(mupath1, "w")
    f2 = open(mupath2, "w")
    whole = len(mulist)
    half = int(whole/4)
    for i in range(0,half*2):
        f1.write(mulist[i])
    for i in range(half*2,whole):
        f2.write(mulist[i])
    f1.close()
    f2.close()
    pathlist1 = []
    pathlist1.append(opath1)
    pathlist2 = []
    pathlist2.append(opath2)
    thr01 = Thread(target=makeup, args=(pathlist1,))
    thr02 = Thread(target=makeup, args=(pathlist2,))
    thr01.start()
    thr02.start()
    thr01.join()
    thr02.join()


if __name__ == "__main__":
    # import time
    # time.sleep(4*60*60)
    output_dir='./vdoutput/recent/'
    domain = "https://bd.yfp1.pro:8869/" 
    # from datetime import datetime
    # while datetime.now().strftime('%Y-%m-%d')=='2026-':
    makenovel2thread(domain, output_dir)