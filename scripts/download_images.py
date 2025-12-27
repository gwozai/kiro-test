#!/usr/bin/env python3
"""
异步下载 Mossia API 图片
下载 50 张图片保存到 daily_images 目录
"""
import asyncio
import aiohttp
import aiofiles
import time
import os

PROXY = 'http://127.0.0.1:7897'
SAVE_DIR = "daily_images"
RECORD_FILE = "daily_images/images_record.txt"
os.makedirs(SAVE_DIR, exist_ok=True)

# 喜欢的图片类型配置
IMAGE_CONFIGS = [
    {"name": "horizontal", "params": {"num": 3, "imageSizeType": 1}},
    {"name": "ai_yes", "params": {"num": 3, "aiType": 2}},
    {"name": "normal", "params": {"num": 3}},
    {"name": "r18_0", "params": {"num": 3, "r18Type": 0}},
    {"name": "r18_1", "params": {"num": 3, "r18Type": 1}},
    {"name": "r18_vertical", "params": {"num": 3, "r18Type": 1, "imageSizeType": 2}},
    {"name": "vertical", "params": {"num": 3, "imageSizeType": 2}},
]

async def download_image(session, img_info, semaphore):
    """异步下载单张图片"""
    async with semaphore:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://www.pixiv.net/'
            }
            async with session.get(img_info["url"], headers=headers, timeout=30) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    filepath = f"{SAVE_DIR}/{img_info['filename']}"
                    async with aiofiles.open(filepath, 'wb') as f:
                        await f.write(content)
                    print(f"  ✅ {img_info['filename']} ({len(content)/1024:.1f} KB)")
                    return img_info
        except Exception as e:
            print(f"  ❌ {img_info['filename']}: {str(e)[:30]}")
        return None

async def fetch_images(session, config):
    """异步获取图片列表"""
    url = "https://api.mossia.top/duckMo"
    images = []
    
    try:
        async with session.get(url, params=config["params"], timeout=15) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("success") and data.get("data"):
                    for item in data["data"]:
                        pid = item.get("pid", "unknown")
                        title = item.get("title", "")
                        r18 = item.get("r18Type", 0)
                        ai = item.get("aiType", 0)
                        urls = item.get("urlsList", [])
                        
                        if urls:
                            img_url = urls[0].get("url")
                            if img_url:
                                ext = img_url.split('.')[-1].split('?')[0][:4]
                                images.append({
                                    "pid": pid,
                                    "title": title,
                                    "r18": r18,
                                    "ai": ai,
                                    "url": img_url,
                                    "type": config["name"],
                                    "filename": f"{config['name']}_{pid}.{ext}"
                                })
    except Exception as e:
        print(f"  获取失败 {config['name']}: {str(e)[:30]}")
    
    return images

async def main():
    print("=" * 60)
    print("异步下载 Mossia API 图片")
    print("=" * 60)
    
    target_count = 50
    downloaded = []
    seen_pids = set()
    
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        # 设置代理
        session._connector._proxy = PROXY
        
        round_num = 0
        while len(downloaded) < target_count:
            round_num += 1
            print(f"\n--- 第 {round_num} 轮 (已下载: {len(downloaded)}/{target_count}) ---")
            
            # 并发获取所有类型的图片列表
            tasks = [fetch_images(session, config) for config in IMAGE_CONFIGS]
            results = await asyncio.gather(*tasks)
            
            # 收集待下载的图片
            to_download = []
            for images in results:
                for img in images:
                    if img["pid"] not in seen_pids and len(downloaded) + len(to_download) < target_count:
                        seen_pids.add(img["pid"])
                        to_download.append(img)
            
            if not to_download:
                print("  没有新图片，等待重试...")
                await asyncio.sleep(2)
                continue
            
            # 并发下载图片（限制并发数）
            semaphore = asyncio.Semaphore(5)
            download_tasks = [download_image(session, img, semaphore) for img in to_download]
            results = await asyncio.gather(*download_tasks)
            
            # 记录成功下载的
            for img in results:
                if img:
                    downloaded.append(img)
            
            await asyncio.sleep(1)
    
    # 保存记录
    print(f"\n{'='*60}")
    print(f"保存记录到 {RECORD_FILE}")
    print(f"{'='*60}")
    
    async with aiofiles.open(RECORD_FILE, 'w', encoding='utf-8') as f:
        await f.write(f"# 图片记录 - 共 {len(downloaded)} 张\n")
        await f.write(f"# 下载时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        await f.write(f"# 格式: 类型 | 文件名 | PID | 标题 | R18 | AI\n")
        await f.write("=" * 80 + "\n\n")
        
        for img in downloaded:
            line = f"{img['type']} | {img['filename']} | {img['pid']} | {img['title'][:30]} | R18:{img['r18']} | AI:{img['ai']}\n"
            await f.write(line)
    
    # 统计
    print(f"\n共下载 {len(downloaded)} 张图片")
    
    type_count = {}
    for img in downloaded:
        t = img['type']
        type_count[t] = type_count.get(t, 0) + 1
    
    print("\n按类型统计:")
    for t, c in sorted(type_count.items()):
        print(f"  {t}: {c} 张")
    
    # 计算总大小
    total_size = sum(
        os.path.getsize(f"{SAVE_DIR}/{f}") 
        for f in os.listdir(SAVE_DIR) 
        if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))
    )
    print(f"\n总大小: {total_size/1024/1024:.1f} MB")

if __name__ == "__main__":
    asyncio.run(main())
