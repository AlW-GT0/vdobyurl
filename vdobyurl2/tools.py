import os

def get_folder_size(folder_path):
    """
    使用 scandir 递归计算文件夹大小（更快）
    """
    total_size = 0
    try:
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file(follow_symlinks=False):
                    try:
                        total_size += entry.stat().st_size
                    except (OSError, FileNotFoundError):
                        pass
                elif entry.is_dir(follow_symlinks=False):
                    total_size += get_folder_size(entry.path)
    except (PermissionError, OSError):
        # 跳过没有权限的文件夹
        pass
    return total_size

def format_size(size_bytes):
    """
    格式化文件大小为易读格式
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"