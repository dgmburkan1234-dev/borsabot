import time
import requests

TELEGRAM_TOKEN = "8984612436:AAGmPceC-rxpm269m9RUa1K4LiD1qOTmenE"
CHAT_ID = "5737893588"

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# Botun mesaj alıp almadığını kontrol eden basit bir yapı
print("Bot aktif, test mesajı gönderiliyor...")
telegram_mesaj_gonder("✅ Bot şu an canlı ve çalışıyor!")

# Railway'in botu "çalışıyor" olarak görmesi için döngü
while True:
    time.sleep(60)
    




