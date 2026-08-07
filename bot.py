import time
import requests

# Telegram Ayarları
TELEGRAM_TOKEN = "SENIN_TELEGRAM_BOT_TOKENIN"
CHAT_ID = "SENIN_CHAT_ID"

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if not response.ok:
            print(f"Telegram mesajı gönderilemedi: {response.text}")
    except Exception as e:
        print(f"Telegram bağlantı hatası: {e}")

def tarama_yap():
    print("Tarama başlatıldı...")
    # Buraya borsa / hisse tarama mantığını ekleyebilirsin
    # Örnek sinyal bulduğunda:
    # telegram_mesaj_gonder("🚨 Sinyal Bulundu: ORLY")
    print("Tarama tamamlandı.")

if __name__ == "__main__":
    print("🤖 Makro Teyitli, Hacimli & Telegram Entegreli Bot Devrede.")
    
    # Başlangıç Test Mesajı
    telegram_mesaj_gonder("🤖 Bot aktif ve bağlantı başarılı! (1 Saatlik ana periyot, 5 dakikalık tarama ile güncellendi)")
    
    try:
        while True:
            tarama_yap()
            time.sleep(300) # 5 Dakika (300 saniye) bekler
    except KeyboardInterrupt:
        print("\nBot durduruldu.")
token : 8984612436:AAGmPceC-rxpm269m9RUa1K4LiD1qOTmenE






