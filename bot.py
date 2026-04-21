import time
import re
import os
import requests
from playwright.sync_api import sync_playwright
from apscheduler.schedulers.blocking import BlockingScheduler

URL = "https://biletyna.pl/inne/Dancing-with-the-Stars-Taniec-z-Gwiazdami"
TELEGRAM_TOKEN = os.environ.get("8604587380:AAGTTgvaIqFd_Ho2uub0-FlQ1X4ifF61OjU")
TELEGRAM_CHAT_ID = os.environ.get("7148066522")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{8604587380:AAGTTgvaIqFd_Ho2uub0-FlQ1X4ifF61OjU}/sendMessage"
    requests.post(url, data={"chat_id": 7148066522, "text": message})

def check_tickets():
    print(f"[CHECK] Sprawdzam... {time.strftime('%H:%M:%S')}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL, wait_until="networkidle", timeout=30000)
            tab = page.locator('a[href="#onsale"]').first
            tab_text = tab.inner_text()
            print(f"[CHECK] Zakładka: {tab_text}")
            match = re.search(r'\((\d+)\)', tab_text)
            count = int(match.group(1)) if match else 0
            browser.close()
            if count > 0:
                send_telegram(f"🎟️ BILETY DOSTĘPNE!\nTaniec z Gwiazdami — {count} wydarzenie(a) w sprzedaży!\n\n{URL}")
            else:
                print("[CHECK] Brak biletów.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    print("Bot uruchomiony. Sprawdza co 60 sekund.")
    check_tickets()
    scheduler = BlockingScheduler()
    scheduler.add_job(check_tickets, "interval", seconds=60)
    scheduler.start()