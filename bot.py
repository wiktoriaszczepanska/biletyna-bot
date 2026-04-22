import time
import re
import os
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

URL = "https://biletyna.pl/inne/Dancing-with-the-Stars-Taniec-z-Gwiazdami"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def check_tickets():
    print(f"[CHECK] Sprawdzam... {time.strftime('%H:%M:%S')}", flush=True)
    try:
        response = requests.get(URL, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        tab = soup.find("a", href="#onsale")
        if not tab:
            print("[ERROR] Nie znaleziono zakładki #onsale", flush=True)
            return
        tab_text = tab.get_text()
        print(f"[CHECK] Zakładka: {tab_text}", flush=True)
        match = re.search(r'\((\d+)\)', tab_text)
        count = int(match.group(1)) if match else 0
        if count > 0:
            send_telegram(f"🎟️ BILETY DOSTĘPNE!\nTaniec z Gwiazdami — {count} wydarzenie(a) w sprzedaży!\n\n{URL}")
        else:
            print("[CHECK] Brak biletów.", flush=True)
    except Exception as e:
        print(f"[ERROR] {e}", flush=True)

if __name__ == "__main__":
    print("Bot uruchomiony. Sprawdza co 60 sekund.", flush=True)
    check_tickets()
    scheduler = BlockingScheduler()
    scheduler.add_job(check_tickets, "interval", seconds=60)
    scheduler.start()
