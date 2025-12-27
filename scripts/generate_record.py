#!/usr/bin/env python3
"""生成图片记录文件"""
import os
import time

SAVE_DIR = "daily_images"
RECORD_FILE = "daily_images/images_record.txt"

def main():
    files = [f for f in os.listdir(SAVE_DIR) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    files.sort()
    
    with open(RECORD_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# 图片记录 - 共 {len(files)} 张\n")
        f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 格式: 类型 | 文件名 | 大小\n")
        f.write("=" * 80 + "\n\n")
        
        type_count = {}
        total_size = 0
        
        for filename in files:
            filepath = f"{SAVE_DIR}/{filename}"
            size = os.path.getsize(filepath)
            total_size += size
            
            # 解析类型
            parts = filename.rsplit('_', 1)
            img_type = parts[0].rsplit('_', 1)[0] if '_' in parts[0] else parts[0]
            
            # 简化类型名
            for t in ['horizontal', 'ai_yes', 'normal', 'r18_0', 'r18_1', 'r18_vertical', 'vertical']:
                if filename.startswith(t):
                    img_type = t
                    break
            
            type_count[img_type] = type_count.get(img_type, 0) + 1
            f.write(f"{img_type} | {filename} | {size/1024:.1f} KB\n")
        
        f.write(f"\n{'='*80}\n")
        f.write(f"# 统计\n")
        f.write(f"总数: {len(files)} 张\n")
        f.write(f"总大小: {total_size/1024/1024:.1f} MB\n\n")
        f.write("按类型:\n")
        for t, c in sorted(type_count.items()):
            f.write(f"  {t}: {c} 张\n")
    
    print(f"记录已保存到 {RECORD_FILE}")
    print(f"共 {len(files)} 张图片, {total_size/1024/1024:.1f} MB")

if __name__ == "__main__":
    main()
