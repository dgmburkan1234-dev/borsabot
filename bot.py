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

# 150 Hisselik Liste
hisseler = [
    "AAPL", "ABNB", "ADI", "ADP", "ADSK", "AEP", "AMAT", "AMD", "AMGN", "AMZN",
    "ANSS", "APP", "ARM", "ASML", "AVGO", "AXON", "AZN", "BKR", "BKNG", "BIIB",
    "CDNS", "CEG", "CHTR", "CMCSA", "COST", "CPRT", "CRWD", "CSX", "CTAS", "CTSH",
    "DASH", "DDOG", "DLTR", "DXCM", "EA", "EXC", "FANG", "FAST", "FTNT", "GEHC",
    "GILD", "GOOG", "GOOGL", "HON", "IDXX", "ILMN", "INKU", "INTC", "INTU", "ISRG",
    "KDP", "KHC", "KLAC", "LRCX", "LULU", "MAR", "MCHP", "MDLZ", "MELI", "META",
    "MGM", "MNST", "MRNA", "MRVL", "MSFT", "MU", "NFLX", "NKE", "NVDA", "NXPI",
    "ODFL", "ORLY", "PANW", "PAYX", "PCAR", "PDD", "PEP", "PYPL", "QCOM", "REGN",
    "ROP", "ROST", "SBUX", "SNPS", "TEAM", "TMUS", "TSLA", "TTD", "TXN", "VRSK",
    "VRTX", "WBD", "WDAY", "XEL", "ZS", "ACGL", "AIG", "AIZ", "ALL", "AON",
    "APA", "APTV", "ACN", "BA", "BAC", "C", "CAT", "CL", "COF", "COP",
    "CVX", "DAL", "DFS", "DIS", "EMR", "EOG", "FDX", "F", "GD", "GE",
    "GM", "GS", "HAL", "HD", "IBM", "JNJ", "JPM", "KO", "LOW", "MA",
    "MCD", "MMM", "MS", "MSI", "NOC", "OXY", "PFE", "PG", "PM", "RTX",
    "SLB", "T", "TGT", "UNH", "UPS", "USB", "V", "VZ", "WFC", "WMT"
]

def telegram_bildirim_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram hatasi: {e}")

def tarama_yap():
    print("150 hisselik tarama başlatılıyor...")
    sinyal_mesaji = ""
    
    for symbol in hisseler:
        try:
            df = yf.download(symbol, period="1mo", interval="1d", progress=False)
            if df.empty or len(df) < 5:
                continue
            
            cikis_fiyati = float(df['Close'].iloc[-1])
            onceki_fiyat = float(df['Close'].iloc[-2])
            
            # Örnek sinyal mantığı (Fiyat bir önceki güne göre yükselişteyse)
            if cikis_fiyati > onceki_fiyat:
                sinyal_mesaji += f"🟢 {symbol} - Fiyat: {cikis_fiyati:.2f}$\n"
                
        except Exception as e:
            print(f"{symbol} taranırken hata: {e}")

    if sinyal_mesaji:
        # Telegram tek mesayda karakter sınırı (4096) olduğu için parça parça da gönderilebilir
        full_mesaj = f"🚀 <b>NASDAQ TARAMA SİNYALLERİ</b> 🚀\n\n{sinyal_mesaji}"
        
        # Mesaj çok uzunsa 4000 karakterlik parçalara bölüp gönder
        if len(full_mesaj) > 4000:
            for i in range(0, len(full_mesaj), 4000):
                telegram_bildirim_gonder(full_mesaj[i:i+4000])
        else:
            telegram_bildirim_gonder(full_mesaj)
            
        print("Telegram'a sinyaller gönderildi!")
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
