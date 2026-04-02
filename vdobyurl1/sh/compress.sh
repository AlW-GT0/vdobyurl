#!/bin/bash

# 源路径（需要压缩的文件夹所在路径）
source_path="/home/dno/mywork/py/bukbyurl1/buk"  # 请将此处替换为实际的源路径

# 目标路径（压缩文件保存路径）
# target_path="/home/dno/mywork/py/.pymnt/sda1/Library/stursc/packed/vdo/NiHActress/NoMos"  # 请将此处替换为实际的目标路径
target_path="$source_path/_pak" #"/home/dno/mywork/py/vdobyurl1/vdoutput/XP/lvmao"
mkdir -p $target_path
# 压缩密码
password="124124sex"

# 检查7zip是否安装
if ! command -v 7z &> /dev/null && ! command -v 7za &> /dev/null; then
    echo "错误：7zip未安装。请先安装7zip："
    echo "Ubuntu/Debian: sudo apt install p7zip-full"
    echo "CentOS/RHEL: sudo yum install p7zip-full"
    exit 1
fi

# 确定7zip命令（优先使用7z，如果不存在则使用7za）
if command -v 7z &> /dev/null; then
    zip_cmd="7z"
else
    zip_cmd="7za"
fi

# 检查源路径是否存在
if [ ! -d "$source_path" ]; then
    echo "错误：源路径 '$source_path' 不存在"
    exit 1
fi

# 创建目标路径（如果不存在）
mkdir -p "$target_path"

# 进入源路径
cd "$source_path" || exit 1

# 遍历源路径下的所有文件夹
for folder in */; do
    # 移除路径末尾的斜杠
    folder_name=$(basename "$folder")
    
    # 跳过空匹配
    if [ -z "$folder_name" ]; then
        continue
    fi
    if [ $folder_name == "_pak" ]; then
        continue
    fi
    
    # 压缩文件名（添加.7z扩展名）
    zip_file="${target_path}/${folder_name}.7z"
    
    echo "正在压缩文件夹: $folder_name"
    
    # 使用7zip压缩文件夹
    if $zip_cmd a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on -p"$password" "$zip_file" "$folder_name" > /dev/null 2>&1; then
        echo "✓ 成功压缩: $folder_name -> ${folder_name}.7z"
    else
        echo "✗ 压缩失败: $folder_name"
    fi
done

echo "压缩完成！所有文件已保存到: $target_path"