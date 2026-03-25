import time
import random
import json
import redis
from datetime import datetime

# Connect to Redis
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.ping()
    print("🟢 NETSEC Data Stream Connected Successfully!")
except Exception as e:
    print("🔴 Redis Error! Is Redis running?", e)
    exit()

# Professional Cyber/Enterprise Logs
LEVELS = ["INFO", "INFO", "INFO", "WARNING", "ERROR"] 
MESSAGES = {
    "INFO": ["Agent_01 Deployed Successfully", "Cache hit rate optimal: 98%", "DB Sync Complete across nodes", "Routing encrypted traffic to Edge-1"],
    "WARNING": ["High CPU load detected on Node-4", "Latency spike (120ms) on API Gateway", "Rate limit approaching for Tenant-A"],
    "ERROR": ["AUTH_FAILURE: Invalid Token Sequence", "Database connection timeout (Port 5432)", "DDoS signature pattern detected on Port 443"]
}

def generate_log():
    print("--- 🚀 Generating Live Telemetry Data ---")
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level = random.choice(LEVELS)
        msg = random.choice(MESSAGES[level])
        ip = f"192.168.1.{random.randint(10, 99)}"
        
        # Structured JSON
        log_data = {
            "timestamp": now,
            "level": level,
            "ip": ip,
            "message": msg
        }
        
        # Push to queue
        r.lpush('log_queue', json.dumps(log_data))
        
        # Terminal par print karo (Video me achha lagega)
        if level == "ERROR":
            print(f"🔴 [CRITICAL] {msg} (Origin: {ip})")
        elif level == "WARNING":
            print(f"🟡 [WARN] {msg}")
        else:
            print(f"🟢 [OK] {msg}")
        
        # Random speed se logs generate karo (0.5 se 2 seconds ke beech)
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    generate_log()