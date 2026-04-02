#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
M3U8视频批量下载脚本
从mulist文件中读取"整数::m3u8链接"格式的记录，按序下载视频
"""

import os
import subprocess
# import sys
import time
from pathlib import Path

def check_ffmpeg():
    """检查ffmpeg是否可用"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def read_mulist(file_path='mulist'):
    """
    读取mulist文件，解析每行内容
    返回: [(整数, m3u8链接), ...] 列表
    """
    videos = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                
                # 解析 "整数::m3u8链接" 格式
                try:
                    # 查找第一个"::"作为分隔符
                    separator = '::'
                    if separator in line:
                        index_part, url_part = line.split(separator, 1)
                        
                        # 处理可能的空格
                        index_part = index_part.strip()
                        url_part = url_part.strip()
                        
                        # 转换为整数
                        video_index = int(index_part)
                        
                        videos.append((video_index, url_part))
                        print(f"✓ 已读取: {video_index} -> {url_part[:50]}...")
                    else:
                        print(f"⚠️ 第{line_num}行格式错误，缺少'::'分隔符: {line}")
                except ValueError as e:
                    print(f"⚠️ 第{line_num}行索引不是有效整数: {line}")
                except Exception as e:
                    print(f"⚠️ 第{line_num}行解析出错: {e}")
    
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 '{file_path}'")
        return None
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        return None
    
    # 按整数排序
    videos.sort(key=lambda x: x[0])
    return videos

def download_video(m3u8_url, output_filename, max_retries=3):
    """
    使用ffmpeg下载m3u8视频
    返回: (成功/失败, 错误信息)
    """
    # 构建ffmpeg命令
    cmd = [
        'ffmpeg',
        '-i', m3u8_url,
        '-c', 'copy',
        '-bsf:a', 'aac_adtstoasc',
        '-y',  # 覆盖已存在的文件
        output_filename
    ]
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"  尝试下载 (第{attempt}次)...")
            
            # 执行ffmpeg命令
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5400  # 超时
            )
            
            if result.returncode == 0:
                # 检查文件是否成功创建且大小>0
                if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
                    return True, None
                else:
                    return False, "文件大小为0"
            else:
                error_msg = result.stderr.decode('utf-8', errors='ignore')[-200:]
                if attempt < max_retries:
                    print(f"  下载失败，{max_retries - attempt}秒后重试...")
                    time.sleep(3)
                else:
                    return False, error_msg
                    
        except subprocess.TimeoutExpired:
            if attempt < max_retries:
                print(f"  下载超时，{max_retries - attempt}秒后重试...")
                time.sleep(3)
            else:
                return False, "下载超时"
                
        except Exception as e:
            if attempt < max_retries:
                print(f"  发生错误: {e}，重试中...")
                time.sleep(3)
            else:
                return False, str(e)
    
    return False, "未知错误"

def check_file_exists(filepath):
    """
    检查文件是否存在且大小>0
    支持Path对象和字符串路径
    """
    if isinstance(filepath, Path):
        return filepath.exists() and filepath.stat().st_size > 0
    else:
        return os.path.exists(filepath) and os.path.getsize(filepath) > 0


def main():
    """主函数"""
    print("=" * 60)
    print("M3U8视频批量下载工具")
    print("=" * 60)
    
    # 检查ffmpeg
    if not check_ffmpeg():
        print("❌ 错误: 未找到ffmpeg")
        print("请确保ffmpeg已安装并添加到系统PATH环境变量中")
        print("下载地址: https://ffmpeg.org/download.html")
        input("按回车键退出...")
        return
    
    print("✓ ffmpeg 检查通过")
    
    # 读取mulist文件
    mulist_path = 'mulist'
    videos = read_mulist(mulist_path)
    
    if videos is None:
        input("按回车键退出...")
        return
    
    if not videos:
        print("❌ 文件中没有找到有效的视频记录")
        input("按回车键退出...")
        return
    
    print(f"\n📊 共找到 {len(videos)} 个视频待下载")
    
    # 创建下载目录（可选）
    download_dir = Path('光荣与梦想')
    download_dir.mkdir(exist_ok=True)
    
    # 统计信息
    success_count = 0
    fail_count = 0
    total = len(videos)
    
    # 按序下载
    print("\n开始下载...")
    print("-" * 60)
    
    for i, (video_index, m3u8_url) in enumerate(videos, 1):
        # 生成文件名：整数.mp4
        filename = f"{video_index}.mp4"
        filepath = f'{download_dir}/{filename}'
        
        print(f"[{i}/{total}] 正在下载: {filepath}")
        print(f"  链接: {m3u8_url[:80]}..." if len(m3u8_url) > 80 else f"  链接: {m3u8_url}")
        
        # 检查文件是否已存在且有效
        if check_file_exists(filepath):
            print(f"  ⏭️  文件已存在且有效，跳过下载")
            skip_count += 1
            success_count += 1  # 算作成功
            continue

        # 下载视频
        success, error_msg = download_video(m3u8_url, str(filepath))
        
        currentime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if success:
            print(f"  ✅{currentime} 下载成功: {filename}")
            success_count += 1
        else:
            print(f"  ❌{currentime} 下载失败: {filename}")
            print(f"     错误: {error_msg}")
            fail_count += 1
        
        # 在视频之间添加短暂延迟，避免请求过快
        if i < total:
            time.sleep(1)
    
    print("-" * 60)
    print("下载完成!")
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {fail_count} 个")
    print(f"📁 文件保存在: {download_dir.absolute()}")
    
    # 如果有失败的任务，询问是否重试
    if fail_count > 0:
        print("\n⚠️  有下载失败的任务")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()