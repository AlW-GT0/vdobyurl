import subprocess
import os
from datetime import datetime

def dloadM3u8(m3u8_list, output_dir="vdoutput"):
    """ 使用 ffmpeg 下载 M3U8 列表中的视频，自动跳过失败的条目。
    Args:
        m3u8_list (list): M3U8 链接列表，如 ["https://.../a.m3u8", ...]
        output_dir (str): 视频保存目录（默认 "vdoutput"）
    """
    current_time = datetime.now()
    time_str = current_time.strftime("%y.%m.%d.%H.%M")#%y.%m.%d.%H.%M.%S
    count = 0
    idx = 0
    lastsuc = False
    for idx, m3u8_url in enumerate(m3u8_list, start=1):
        # 这部分针对记录两个m3u8的情况
        if lastsuc:
            lastsuc = False
            continue
        
        parts = m3u8_url.split('::',1)
        output_path = os.path.join(output_dir, f"{time_str}_{idx} {parts[0]}.mp4")
        print(f"{datetime.now().strftime("%H:%M")}正在下载 {idx}/{len(m3u8_list)}: {m3u8_url}")
        try: # 调用 ffmpeg 下载（超时设为  秒）
            subprocess.run(
                [
                    "ffmpeg",
                    "-i", parts[1],      # 输入 M3U8 链接
                    "-c", "copy",        # 直接复制流（避免转码）
                    "-bsf:a", "aac_adtstoasc",  # 修复 AAC 音频流
                    output_path          # 输出文件路径
                ],
                check=True,              # 如果 ffmpeg 返回非零码则抛出异常
                timeout=10000,             # 超时时间（秒）
                # stdout=subprocess.PIPE,  # 隐藏输出日志
                stderr=subprocess.PIPE
            )
            print(f"{datetime.now().strftime("%H:%M")}下载成功: {output_path}")
            count += 1
            lastsuc = (idx%2!=0)
                    
        except subprocess.TimeoutExpired:
            try:
                os.remove(output_path)
                print(f"{datetime.now().strftime("%H:%M")}超时跳过: {m3u8_url}")
            except Exception as e:
                print(f"{datetime.now().strftime("%H:%M")}删除失败: {e}")
            continue
        except subprocess.CalledProcessError as e:
            try:
                os.remove(output_path)
                print(f"{datetime.now().strftime("%H:%M")}下载失败: {m3u8_url} (错误: {e.stderr.decode('utf-8')[:200]}...)")
            except Exception as e:
                print(f"删除失败: {e}")
            continue
    print(f"{idx/2}个任务完成{count}个！")


def makeup(makeuplist):
    for path in makeuplist:
        print(f'fetch vdo from {path}')
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
    # import time
    # time.sleep(24*60*60)
    makeuplist = [
        './vdoutput/recent/2026-04-15/1/',
        './vdoutput/recent/2026-04-15/2/',
        ]
    makeup(makeuplist)

