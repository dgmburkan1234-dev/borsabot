import time
import requests
import pandas as pd
import yfinance as yf

# Ayarlar
TELEGRAM_TOKEN = "8984612436:AAGmPceC-rxpm269m9RUa1K4LiD1qOTmenE"
CHAT_ID = "5737893588"
hisseler = ["ORLY", "PFE", "HD", "AMCR", "ONON", "FAST", "LULU", "BKR", "PDD", "CSCO", "HON", "CHWY", "PYPL", "TREX"]

def telegram_bildirim_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
    requests.post(url, json=payload, timeout=5)

def makro_piyasa_kontrol():
    try:
        vix = yf.download("^VIX", period="5d", interval="1d", progress=False)
        if vix.empty: return True
        if isinstance(vix.columns, pd.MultiIndex): vix.columns = vix.columns.get_level_values(0)
        vix_son = vix["Close"].iloc[-1]
        vix_onceki = vix["Close"].iloc[-2]
        return vix_son <= vix_onceki * 1.02
    except: return True

def tarama_yap():
    print(f"\n--- Yeni Tarama: {pd.Timestamp.now()} ---")
    if not makro_piyasa_kontrol():
        print("⚠️ Makro Uyarı: VIX hareketli, long filtreler askıda.")
        return

    for sembol in hisseler:
        try:
            veri_4h = yf.download(sembol, period="60d", interval="1h", progress=False)
            if veri_4h.empty: continue
            if isinstance(veri_4h.columns, pd.MultiIndex): veri_4h.columns = veri_4h.columns.get_level_values(0)

            son_kapanis_4h = veri_4h["Close"].iloc[-1]
            direncler_4h = veri_4h["High"].iloc[-40:-10].max()
            destekler_4h = veri_4h["Low"].iloc[-40:-10].min()
            onceki_tepe_4h = veri_4h["High"].iloc[-10:-1].max()
            guncel_yuksek_4h = veri_4h["High"].iloc[-1]

            puan_4h = 0
            if abs(son_kapanis_4h - destekler_4h) / destekler_4h < 0.03 or abs(son_kapanis_4h - direncler_4h) / direncler_4h < 0.03: puan_4h += 1
            if guncel_yuksek_4h > onceki_tepe_4h: puan_4h += 2

            if puan_4h < 3: continue

            # 15m Kontrolü
            veri_15m = yf.download(sembol, period="5d", interval="15m", progress=False)
            if veri_15m.empty: continue
            if isinstance(veri_15m.columns, pd.MultiIndex): veri_15m.columns = veri_15m.columns.get_level_values(0)
            
            ortalama_hacim = veri_15m["Volume"].iloc[-20:-1].mean()
            if veri_15m["Volume"].iloc[-1] > ortalama_hacim:
                mesaj = f"🎯🚀 SNAYPIR LONG ONAYLANDI!\nHisse: {sembol}\nFiyat: {son_kapanis_4h:.2f}"
                telegram_bildirim_gonder(mesaj)
                print(mesaj)
        except: continue

# Bot Başlangıç
print("🤖 Snaypır Botu Stratejisi Devrede!")
telegram_bildirim_gonder("🤖 Snaypır Botu strateji modunda başlatıldı!")

while True:
    tarama_yap()
    time.sleep(900) # 15 Dakika
    


