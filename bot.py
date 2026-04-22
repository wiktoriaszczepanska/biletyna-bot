import time
import re
import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
URL_PAGE = "https://biletyna.pl/inne/Dancing-with-the-Stars-Taniec-z-Gwiazdami"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def check_tickets():
    print(f"[CHECK] Sprawdzam... {time.strftime('%H:%M:%S')}", flush=True)
    try:
        # Szukamy wydarzeń przez API biletyny
        response = requests.get(
            "https://biletyna.pl/api/v1/events",
            params={"q": "Taniec z Gwiazdami", "status": "onsale"},
            headers={"Accept": "application/json"},
            timeout=30
        )
        print(f"[CHECK] Status: {response.status_code}", flush=True)
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get("events", data if isinstance(data, list) else []))
            print(f"[CHECK] Znaleziono: {count}", flush=True)
            if count > 0:
                send_telegram(f"🎟️ BILETY DOSTĘPNE!\nTaniec z Gwiazdami — {count} wydarzenie(a) w sprzedaży!\n\n{URL_PAGE}")
            else:
                print("[CHECK] Brak biletów.", flush=True)
        else:
            print(f"[CHECK] Odpowiedź: {response.text[:200]}", flush=True)

    except Exception as e:
        print(f"[ERROR] {e}", flush=True)

if __name__ == "__main__":
    print("Bot uruchomiony. Sprawdza co 3 minuty.", flush=True)
    check_tickets()
    scheduler = BlockingScheduler()
    scheduler.add_job(check_tickets, "interval", seconds=180)
    scheduler.start()
