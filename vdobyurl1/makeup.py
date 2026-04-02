from dloadVdo import dloadM3u8
import time

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

if __name__ == "__main__":
    # time.sleep(24*60*60)
    makeuplist = [
        './vdoutput/NiHActress/NoMos/168/',
        ]
    makeup(makeuplist)

