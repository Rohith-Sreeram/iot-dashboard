import requests
import time
import random

# ==========================================
# CONFIGURATION
# ==========================================
DEVICE_NAME = "iot_dashboard_esp32_unique_9923" 
SYNC_INTERVAL = 5 

def simulate_cloud_esp32():
    print(f"🚀 Cloud Simulator active for: {DEVICE_NAME}")
    
    entered = 0
    left = 0
    
    try:
        while True:
            # 1. Check for Cloud Reset
            try:
                check_url = f"https://dweet.io/get/latest/dweet/for/{DEVICE_NAME}"
                res = requests.get(check_url, timeout=3).json()
                if res.get("this") == "succeeded" and len(res.get("with", [])) > 0:
                    if res["with"][0]["content"].get("command") == "reset":
                        print("🔔 Cloud Reset Detected!")
                        entered = 0
                        left = 0
            except:
                pass

            # 2. Simulate counts
            if random.random() > 0.6: entered += 1
            present = max(0, entered - left)
            if present > 0 and random.random() > 0.8: left += 1
            present = max(0, entered - left)
            
            # 3. Push to Cloud
            payload = {"entered": entered, "left": left, "present": present}
            requests.post(f"https://dweet.io/dweet/for/{DEVICE_NAME}", json=payload, timeout=3)
            print(f"Syncing: In={entered | Out={left} | Active={present}")
            
            time.sleep(SYNC_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    simulate_cloud_esp32()
