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

# Flask sunucusunu arka planda başlatıyoruz (Render health-check)
threading.Thread(target=run_flask, daemon=True).start()

# Yahoo Finance istekleri için taranma başlığı
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

# Ayarlar
TELEGRAM_TOKEN = "8984612436:AAGmPceC-rxpm269m9RUa1K4LiD1qOTmenE"
CHAT_ID = "5737893588"

# 150 NASDAQ Hissesi
nasdaq_hisseleri = [
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

# 100 BIST Hissesi (.IS eklentili)
bist_hisseleri = [
    "AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", "AKFYE.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS",
    "ALBRK.IS", "ALFAS.IS", "ANSGR.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BERA.IS", "BIENP.IS", "BIMAS.IS", "BIOEN.IS",
    "BOBET.IS", "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS", "CIMSA.IS", "CWENE.IS", "DOAS.IS", "DOHOL.IS",
    "ECILC.IS", "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS", "EUPWR.IS", "EUREK.IS", "FROTO.IS",
    "GARAN.IS", "GESAN.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HEKTS.IS", "IMASM.IS", "IPEKE.IS", "ISCTR.IS", "ISGYO.IS",
    "ISMEN.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KONTR.IS", "KORDS.IS", "KOZAL.IS", "KOZAA.IS", "KRDMD.IS", "KZBGY.IS",
    "MAVI.IS", "MGNTS.IS", "MHMTR.IS", "MIATK.IS", "MGROS.IS", "ODAS.IS", "OTKAR.IS", "OYAKC.IS", "PETKM.IS", "PGSUS.IS",
    "PSGYO.IS", "REEDR.IS", "SAHOL.IS", "SASA.IS", "SDTTR.IS", "SISE.IS", "SKBNK.IS", "SMRTG.IS", "SOKM.IS", "TABGD.IS",
    "TAVHL.IS", "TCELL.IS", "THYAO.IS", "TKFEN.IS", "TOASO.IS", "TSKB.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS",
    "TURSG.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"
]

def telegram_bildirim_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram hatasi: {e}")

def piyasa_tara(hisse_listesi, piyasa_adi):
    print(f"{piyasa_adi} taraması başlatılıyor ({len(hisse_listesi)} hisse)...")
    sinyal_mesaji = ""
    
    for symbol in hisse_listesi:
        try:
            ticker = yf.Ticker(symbol, session=session)
            df = ticker.history(period="1mo", interval="1d")
            
            if df.empty or len(df) < 5:
                time.sleep(0.2)
                continue
            
            cikis_fiyati = float(df['Close'].iloc[-1])
            onceki_fiyat = float(df['Close'].iloc[-2])
            
            # Yükseliş kontrolü
            if cikis_fiyati > onceki_fiyat:
                temiz_sembol = symbol.replace(".IS", "")
                para_birimi = "₺" if ".IS" in symbol else "$"
                sinyal_mesaji += f"🟢 {temiz_sembol} - Fiyat: {cikis_fiyati:.2f}{para_birimi}\n"
                
            time.sleep(0.2)
                
        except Exception as e:
            print(f"{symbol} taranırken hata: {e}")
            time.sleep(0.3)

    if sinyal_mesaji:
        full_mesaj = f"🚀 <b>{piyasa_adi} TARAMA SİNYALLERİ</b> 🚀\n\n{sinyal_mesaji}"
        
        if len(full_mesaj) > 4000:
            for i in range(0, len(full_mesaj), 4000):
                telegram_bildirim_gonder(full_mesaj[i:i+4000])
        else:
            telegram_bildirim_gonder(full_mesaj)
            
        print(f"{piyasa_adi} sinyalleri Telegram'a gönderildi!")
    else:
        print(f"{piyasa_adi} için yeni sinyal bulunamadı.")

def genel_tarama():
    piyasa_tara(nasdaq_hisseleri, "NASDAQ")
    piyasa_tara(bist_hisseleri, "BIST 100")

# Otomatik tarama döngüsü (Her 1 saatte bir çalışır)
def tarama_dongusu():
    while True:
        genel_tarama()
        time.sleep(3600)

# Taramayı arka planda başlat
threading.Thread(target=tarama_dongusu, daemon=True).start()

# Sunucunun kapanmaması için ana thread'i açık tut
while True:
    time.sleep(60)
