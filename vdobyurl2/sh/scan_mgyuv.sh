#!/bin/bash
# ============================================================
# scan_magicyuv.sh
# 递归扫描指定目录下的所有 .mp4 文件，检测是否包含
# MagicYUV 视频流（CVE-2026-8461 攻击面）。
# 用法:  bash scan_magicyuv.sh [目录路径]
# 默认目录: 当前目录 (.)
# ============================================================

set -u

TARGET_DIR="${1:-.}"
LOG_FILE="$(pwd)/_magicyuv_scan_report.txt"
SUSPECT_DIR="$(pwd)/magicyuv_suspects"

# 颜色（终端可用时）
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 计数器
total=0
clean=0
suspect=0
error=0

# 临时文件
tmp_report="$(mktemp)"
trap 'rm -f "$tmp_report"' EXIT

echo "============================================================"
echo "  MagicYUV 扫描器  (CVE-2026-8461 攻击面检测)"
echo "  扫描目录: $TARGET_DIR"
echo "  报告文件: $LOG_FILE"
echo "============================================================"
echo ""

# 初始化报告
{
    echo "MagicYUV 扫描报告"
    echo "扫描时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "扫描目录: $TARGET_DIR"
    echo "============================================================"
    echo ""
} > "$LOG_FILE"

# 创建可疑文件隔离目录
mkdir -p "$SUSPECT_DIR"

# 查找所有 mp4 文件（大小写不敏感）
mapfile -d '' files < <(find "$TARGET_DIR" -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mkv" -o -iname "*.mov" \) -print0 2>/dev/null)

total=${#files[@]}

if [ "$total" -eq 0 ]; then
    echo "未找到任何视频文件 (.mp4/.avi/.mkv/.mov)"
    echo "总文件数: 0" | tee -a "$LOG_FILE"
    exit 0
fi

echo "找到 $total 个视频文件，开始扫描..."
echo ""

# 进度条函数
progress_bar() {
    local current=$1
    local total=$2
    local width=40
    local percent=$((current * 100 / total))
    local filled=$((current * width / total))
    printf "\r["
    for ((i=0; i<filled; i++)); do printf "="; done
    for ((i=filled; i<width; i++)); do printf " "; done
    printf "] %d/%d (%d%%)" "$current" "$total" "$percent"
}

current=0

for f in "${files[@]}"; do
    current=$((current + 1))
    progress_bar "$current" "$total"

    # 用 ffprobe 更轻量、更可靠地检测视频流编码
    # 如果 ffprobe 不可用则回退到 ffmpeg
    if command -v ffprobe >/dev/null 2>&1; then
        codec_info=$(ffprobe -v quiet -select_streams v:0 \
            -show_entries stream=codec_name,codec_tag_string \
            -of default=noprint_wrappers=1:nokey=1 "$f" 2>/dev/null)
        rc=$?
    else
        codec_info=$(ffmpeg -i "$f" 2>&1 | grep -i 'Video:' | head -1)
        rc=0
    fi

    # 提取 codec 名称（ffprobe 输出第一行是 codec_name）
    codec_name=$(echo "$codec_info" | head -1 | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')

    # 检查是否是 magicyuv（包括变体拼写）
    if echo "$codec_name" | grep -qi 'magicyuv\|magicyu'; then
        suspect=$((suspect + 1))
        rel_path="${f#$TARGET_DIR/}"
        printf "\n  ${RED}[!] 发现 MagicYUV 流${NC}: %s\n" "$rel_path"
        printf "      编  码: %s\n" "$codec_name"

        # 记录到报告
        {
            echo "[SUSPECT] $f"
            echo "  编码: $codec_name"
            echo "  检测时间: $(date '+%Y-%m-%d %H:%M:%S')"
            echo "  ---"
        } >> "$LOG_FILE"

        # 复制可疑文件到隔离目录（保留目录结构）
        rel_dir=$(dirname "${f#$TARGET_DIR/}")
        mkdir -p "$SUSPECT_DIR/$rel_dir"
        cp "$f" "$SUSPECT_DIR/$rel_dir/" 2>/dev/null && \
            echo "  ${YELLOW}  → 已复制到: $SUSPECT_DIR/$rel_dir/$(basename "$f")${NC}"

    elif [ "$rc" -ne 0 ] || [ -z "$codec_name" ]; then
        error=$((error + 1))
        rel_path="${f#$TARGET_DIR/}"
        printf "\n  ${YELLOW}[?] 无法解析${NC}: %s\n" "$rel_path"
        {
            echo "[ERROR] $f"
            echo "  原因: ffprobe/ffmpeg 无法解析该文件"
            echo "  ---"
        } >> "$LOG_FILE"
    else
        clean=$((clean + 1))
        # 干净文件只记 codec 到报告（可选，量大时可注释掉）
        rel_path="${f#$TARGET_DIR/}"
        {
            echo "[CLEAN] $rel_path  (codec: $codec_name)"
        } >> "$tmp_report"
    fi
done

# 清掉进度行
printf "\n\n"

# ===================== 汇总报告 =====================
echo "============================================================"
echo -e "  ${CYAN}扫描完成 — 汇总${NC}"
echo "============================================================"
echo -e "  扫描目录       : $TARGET_DIR"
echo -e "  总文件数       : $total"
echo -e "  ${GREEN}干净文件       : $clean${NC}"
echo -e "  ${RED}可疑文件(MagicYUV): $suspect${NC}"
echo -e "  ${YELLOW}解析失败       : $error${NC}"
echo "============================================================"
echo ""
echo "详细报告: $LOG_FILE"
if [ "$suspect" -gt 0 ]; then
    echo -e "${RED}可疑文件已复制到: $SUSPECT_DIR${NC}"
fi
echo ""

# 追加汇总到报告
{
    echo ""
    echo "============================================================"
    echo "汇总"
    echo "============================================================"
    echo "总文件数: $total"
    echo "干净文件: $clean"
    echo "可疑文件(MagicYUV): $suspect"
    echo "解析失败: $error"
    echo "扫描结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
} >> "$LOG_FILE"

# 把 clean 列表也追加进报告
if [ -s "$tmp_report" ]; then
    echo "" >> "$LOG_FILE"
    echo "------ 干净文件列表 ------" >> "$LOG_FILE"
    cat "$tmp_report" >> "$LOG_FILE"
fi

# 如果没找到可疑文件，删掉空目录
if [ "$suspect" -eq 0 ]; then
    rmdir "$SUSPECT_DIR" 2>/dev/null
fi

# 退出码：发现可疑文件返回 1，方便脚本串联
[ "$suspect" -gt 0 ] && exit 1 || exit 0
