import os
from threading import Thread

import sched
import time
from datetime import datetime, timedelta

from getVdolist import getVdolist2_4novel
from makeup import makeup, distribute_mulist
from tools import get_folder_size, format_size 

def donothing():
    return None

def makenovel(output_dir, divide_part=2):
    opath = getVdolist2_4novel(output_dir)
    makeuplist = distribute_mulist(opath, divide_part)
    
    thrds = []
    pathlists = []
    for i in range(divide_part):
        pathlist = []
        pathlist.append(makeuplist[i])
        pathlists.append(pathlist[:]) # 通过切片深拷贝
        thrds.append(Thread(target=makeup, args=(pathlists[i],)))
        thrds[i].start()
    # makeup(makeuplist)
    for i in range(divide_part):
        thrds[i].join()
    print(f'{divide_part}个线程执行完毕\n')
    
    size_byt = get_folder_size(opath)
    print(f'Get detail information in {opath}')
    print(f'Size of which: {format_size(size_byt)}')
    return f'{format_size(size_byt)}'

def insistent_making_novel(output_dir):
    schdler = sched.scheduler(time.time, time.sleep)
    target_time = datetime.now().replace(minute=3, second=0, microsecond=0) + timedelta(hours=1) # .timestamp()
    print(f'设置运行时间：{target_time}')
    # # 如果已经过了3min，则改为下一小时
    # if datetime.now() >= target_time:
    #     target_time += timedelta(hours=1)

    while True:
        target_timestamp = target_time.timestamp()
        schdler.enterabs(target_timestamp, 1, donothing)
        target_time += timedelta(hours=1)
        print(f'设置完毕，将于预设时间继续运行...')

        schdler.run()
        result_size = makenovel(output_dir)
        if result_size != '0.00 B':
            break
        print(f'Size: {result_size}, it might need remake.')
        if datetime.now() >= target_time:
            target_time += timedelta(hours=1)
            print(f'设置运行时间：{target_time}')


if __name__ == "__main__":
    output_dir = './vdoutput/recent/'
    # domain = "https://sz3u.yep1.pro:8869/"
    # # 本版本(v2.1)中将makenovel优化为动态获取domain
    # from datetime import datetime
    # while datetime.now().strftime('%Y-%m-%d')=='2026-':
    makenovel(output_dir) # insistent_making_novel(output_dir)
