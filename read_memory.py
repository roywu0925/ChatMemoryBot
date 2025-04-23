# read_memory.py

import redis
import json

# Redis 連線參數（預設本地端）
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 替換這裡的 session_id（你原本用的是 "my-session"）
session_id = "my-session"
redis_key = f"lc-chat-{session_id}"

# 抓出這個 session 的所有訊息（Redis 是 list 結構）
messages = r.lrange(redis_key, 0, -1)

print(f"\n🧠 Redis 中 '{session_id}' 的記憶紀錄：\n")

for m in messages:
    parsed = json.loads(m)  # 每條訊息都是一段 JSON
    role = parsed.get("type", "unknown")
    content = parsed.get("data", "")
    
    if role == "human":
        print(f"🧑 你：{content}")
    elif role == "ai":
        print(f"🤖 AI：{content}")
    else:
        print(f"❓ 未知：{content}")
