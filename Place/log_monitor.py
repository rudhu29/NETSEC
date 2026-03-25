import redis
import json
import requests  # Nayi library add ki

# YAHAN APNA DISCORD WEBHOOK URL PASTE KARO 👇
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1486252109090394202/e0nvLI8QBEBF-rtTgoYVWbg4zRe8kHbpSgMcY3WX6GYfLP2kX0YA17wnwQ_WNDLi7SvV"

try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.ping()
    print("--- Security Monitor Activated ---")
    print("Waiting for logs from Redis Queue...\n")
except Exception as e:
    print("Redis Error!", e)
    exit()

error_count = 0

def send_discord_alert(message):
    """Ye function Discord par alert bhejta hai"""
    data = {
        "content": f"🚨 **CRITICAL ALERT:** {message} 🚨\n@everyone Server is under heavy load, please check immediately!"
    }
    # Webhook par POST request bhej rahe hain
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def monitor_logs():
    global error_count
    while True:
        result = r.brpop('log_queue', timeout=0) 
        
        if result:
            queue_name, data_string = result
            queue_name, data_string = result
            
            # --- NAYI 2 LINES DASHBOARD KE LIYE ---
            r.lpush('recent_logs', data_string) # Naya log history mein dalo
            r.ltrim('recent_logs', 0, 19)       # Sirf latest 20 logs save rakho
            # --------------------------------------

            log_data = json.loads(data_string)
            log_data = json.loads(data_string)
            
            if log_data['level'] == 'ERROR':
                error_count += 1
                print(f"🚨 [ALERT] ERROR DETECTED: {log_data['message']} (From IP: {log_data['ip']})")
                
                # Agar 3 errors lagatar aayein, toh DISCORD par alert bhejo!
                if error_count >= 3:
                    alert_msg = f"System detected multiple errors including: {log_data['message']} from IP: {log_data['ip']}"
                    
                    print("\n" + "="*50)
                    print("🔥 CRITICAL ALERT: SYSTEM UNDER HEAVY LOAD OR ATTACK! 🔥")
                    print("Triggering Discord Webhook...")
                    
                    # Call the function to send the message
                    send_discord_alert(alert_msg)
                    
                    print("="*50 + "\n")
                    error_count = 0 
            else:
                print(f"✅ [OK] {log_data['level']}: {log_data['message']}")

if __name__ == "__main__":
    monitor_logs()