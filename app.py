import requests
import os
import time
import hashlib

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.bls-appointments.com/izmir"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

last_hash = None

def telegram(msg):
    if not TOKEN or not CHAT_ID:
        print("Missing TOKEN or CHAT_ID")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_page():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=10)
        return r.text
    except Exception as e:
        print("Request error:", e)
        return ""

def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()

print("Bot started...")

while True:
    html = get_page()

    if html:
        current_hash = hash_text(html)

        if last_hash is None:
            last_hash = current_hash
            print("Initial snapshot saved")

        elif current_hash != last_hash:
            print("CHANGE DETECTED!")
            telegram("🔔 Sayfa değişti! İzmir BLS randevu sayfası güncellenmiş olabilir.")
            last_hash = current_hash
        else:
            print("No change")

    time.sleep(60)