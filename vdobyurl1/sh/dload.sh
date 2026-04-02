#!/bin/bash

# 检查输入文件是否存在
INPUT_FILE="mulist.txt"
if [ ! -f "$INPUT_FILE" ]; then
    echo "错误：找不到输入文件 $INPUT_FILE"
    exit 1
fi
# 获取当前时间（格式：video2025.06.05.10.39.46）
TIMESTAMP="video$(date +"%Y.%m.%d.%H.%M.%S")"
i=1  # 自增序号起始值

# 逐行处理每个 .m3u8 链接
while IFS= read -r line || [[ -n "$line" ]]; do
    # 跳过空行和注释行（以 # 开头）
    if [[ -z "$line" || "$line" == \#* ]]; then
        continue
    fi

    echo "正在下载: $line"

    # 生成文件名（如 video2025.06.05.10.39.46_1.mp4）
    output_file="../vdoutput/PREG/yf/${TIMESTAMP}_${i}.mp4"

    # 使用 ffmpeg 下载
    ffmpeg -nostdin -i "$line" -c copy "$output_file" -y

    if [ $? -eq 0 ]; then
        echo "下载完成: $output_file"
        ((i++))  # 序号自增
    else
        echo "下载失败: $line"
    fi

done < "$INPUT_FILE"

echo "所有任务处理完毕！"