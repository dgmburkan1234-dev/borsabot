import os
import threading
import time
import requests
import pandas as pd
import yfinance as yf
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Flask sunucusunu arka planda başlatıyoruz
threading.Thread(target=run_flask, daemon=True).start()

# Ayarlar
TELEGRAM_TOKEN = "8984612436:AAGmPceC-rxpm269m9RUa1K4LiD1qOTmenE"
CHAT_ID = "5737893588"

hisseler = [
    "AAPL", "ABNB", "ADI", "AEP", "AMD", "AMX", "ARM", "BKNG", 
    "CEG", "COIN", "COST", "CTAS", "DLTR", "IBM", "INTC", "INTU", 
    "ISRG", "MCD", "META", "MRVL", "MU", "NKE", "ODFL", "PAYX", 
    "PCAR", "PEP", "QCOM", "TMUS", "VRSK", "VRTX", "WBD", "ZS"
]

def telegram_bildirim_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram hatasi: {e}")

def tarama_yap():
    print("Tarama başlatılıyor...")
    sinyal_mesaji = ""
    
    for symbol in hisseler:
        try:
            df = yf.download(symbol, period="1 mo", interval="1d", progress=False)
            if df.empty or len(df) < 5:
                continue
            
            # Örnek sinyal kontrolü (Kendi indikatör/strateji mantığınıza göre düzenleyebilirsiniz)
            cikis_fiyati = float(df['Close'].iloc[-1])
            onceki_fiyat = float(df['Close'].iloc[-2])
            
            # Fiyat yükselişteyse örnek sinyal metni ekler
            if cikis_fiyati > onceki_fiyat:
                sinyal_mesaji += f"🟢 {symbol} - Fiyat: {cikis_fiyati:.2f}$\n"
                
        except Exception as e:
            print(f"{symbol} taranırken hata: {e}")

    if sinyal_mesaji:
        full_mesaj = f"🚀 <b>NASDAQ TARAMA SİNYALLERİ</b> 🚀\n\n{sinyal_mesaji}"
        telegram_bildirim_gonder(full_mesaj)
        print("Telegram'a sinyal gönderildi!")
    else:
        print("Yeni sinyal bulunamadı.")

# Otomatik tarama döngüsü (Her 1 saatte bir çalışır)
def tarama_dongusu():
    while True:
        tarama_yap()
        time.sleep(3600) # 3600 saniye = 1 saat

# Taramayı arka planda başlat
threading.Thread(target=tarama_dongusu, daemon=True).start()

# Sunucunun kapanmaması için ana thread'i açık tut
while True:
    time.sleep(60)
