<<<<<<< HEAD
# Bot Başlatma ve Döngü
print(
    "🤖 Makro Teyitli, Hacimli & Telegram Entegreli Snaypir Botu Devrede (Ana"
    " periyot: 1 Saat, Kontrol: 5 Dakika)."
)

# Telegram Bağlantı Testi
try:
  telegram_mesaj_gonder(
      "🤖 Bot aktif ve bağlantı başarılı! (1 Saatlik ana periyot, 5 dakikalık"
      " tarama ile güncellendi)"
  )
  print("Test mesajı Telegram'a gönderildi.")
except Exception as e:
  print(f"Test mesajı gönderilemedi: {e}")

try:
  while True:
    tarama_yap()
    time.sleep(300)  # 5 Dakika (300 saniye) bekler
except KeyboardInterrupt:
  print("\nBot durduruldu.")
  
=======
import time
import pandas as pd
import yfinance as yf

# TradingView takip listen
hisseler = [
    "ORLY",
    "PFE",
    "HD",
    "AMCR",
    "ONON",
    "FAST",
    "LULU",
    "BKR",
    "PDD",
    "CSCO",
    "HON",
    "CHWY",
    "PYPL",
    "TREX",
]

# Telegram Bilgilerin (Güncellendi)
TELEGRAM_TOKEN = "8984612436:AAGmPceC-rxpm269mRUa1K4LiD1qOTmenE"
TELEGRAM_CHAT_ID = "5737893588"


def telegram_bildirim_gonder(mesaj):
  """Yakalanan sinyalleri doğrudan Telegram hesabına gönderir."""
  try:
    import requests

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
    requests.post(url, json=payload, timeout=5)
  except Exception as e:
    print(f"Telegram mesajı gönderilemedi: {e}")


def makro_piyasa_kontrol():
  """VIX ve DXY bazlı makro piyasa yönünü süzer.

  VIX patlaması varsa long işlemleri korumaya alır.
  """
  try:
    vix = yf.download("^VIX", period="5d", interval="1d", progress=False)
    dxy = yf.download("DX-Y.NYB", period="5d", interval="1d", progress=False)

    if vix.empty or dxy.empty:
      return True

    if isinstance(vix.columns, pd.MultiIndex):
      vix.columns = vix.columns.get_level_values(0)
    if isinstance(dxy.columns, pd.MultiIndex):
      dxy.columns = dxy.columns.get_level_values(0)

    vix_son = vix["Close"].iloc[-1]
    vix_onceki = vix["Close"].iloc[-2]

    # VIX ani sıçrama yapmamışsa piyasa long için uygundur
    vix_durumu_iyi = vix_son <= vix_onceki * 1.02
    return vix_durumu_iyi
  except Exception:
    return True


def tarama_yap():
  zaman_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
  print(f"\n--- Yeni Tarama Başlangıcı: {zaman_str} ---")

  # 1. Adım: Makro Filtre (VIX Korku Endeksi Kontrolü)
  makro_onay = makro_piyasa_kontrol()
  if not makro_onay:
    print(
        "⚠️ Makro Uyarı: VIX (Korku Endeksi) hareketli, long filtreler askıya"
        " alındı."
    )
    return

  bulunan_signal = False

  for sembol in hisseler:
    try:
      # 2. Adım: 4 Saatlik (4H) Ana Trend ve SR Flip / Likidite Analizi
      veri_4h = yf.download(sembol, period="60d", interval="1h", progress=False)
      if veri_4h.empty:
        continue
      if isinstance(veri_4h.columns, pd.MultiIndex):
        veri_4h.columns = veri_4h.columns.get_level_values(0)

      son_kapanis_4h = veri_4h["Close"].iloc[-1]
      direncler_4h = veri_4h["High"].iloc[-40:-10].max()
      destekler_4h = veri_4h["Low"].iloc[-40:-10].min()
      onceki_tepe_4h = veri_4h["High"].iloc[-10:-1].max()
      guncel_yuksek_4h = veri_4h["High"].iloc[-1]

      puan_4h = 0
      sr_flip_4h = (
          abs(son_kapanis_4h - destekler_4h) / destekler_4h < 0.03
          or abs(son_kapanis_4h - direncler_4h) / direncler_4h < 0.03
      )
      if sr_flip_4h:
        puan_4h += 1
      if guncel_yuksek_4h > onceki_tepe_4h:
        puan_4h += 2

      if puan_4h < 3:
        continue

      # 3. Adım: 15 Dakikalık (15m) Snaypır Tetik + Hacim Teyidi
      veri_15m = yf.download(
          sembol, period="5d", interval="15m", progress=False
      )
      if veri_15m.empty:
        continue
      if isinstance(veri_15m.columns, pd.MultiIndex):
        veri_15m.columns = veri_15m.columns.get_level_values(0)

      destekler_15m = veri_15m["Low"].iloc[-40:-10].min()
      onceki_tepe_15m = veri_15m["High"].iloc[-10:-1].max()
      guncel_yuksek_15m = veri_15m["High"].iloc[-1]
      son_kapanis_15m = veri_15m["Close"].iloc[-1]

      # Hacim Teyidi: Son mumdaki hacim ortalamanın üzerinde mi?
      ortalama_hacim = veri_15m["Volume"].iloc[-20:-1].mean()
      guncel_hacim = veri_15m["Volume"].iloc[-1]
      hacim_onayi = guncel_hacim > ortalama_hacim

      puan_15m = 0
      sr_flip_15m = (
          abs(son_kapanis_15m - destekler_15m) / destekler_15m < 0.015
      )
      if sr_flip_15m:
        puan_15m += 1
      if guncel_yuksek_15m > onceki_tepe_15m:
        puan_15m += 2

      # Tüm şartlar eksiksiz sağlanmalı
      if puan_15m == 3 and hacim_onayi:
        mesaj = (
            f"🎯🚀 *SNAYPIR LONG ONAYLANDI!*\n"
            f"• Hisse: `{sembol}`\n"
            f"• 4H Fiyat: `{son_kapanis_4h:.2f}`\n"
            f"• Durum: VIX Onaylı + Hacimli Kırılım"
        )
        print(mesaj)
        telegram_bildirim_gonder(mesaj)
        bulunan_signal = True

    except Exception:
      pass

  if not bulunan_signal:
    print("Bu turda tüm makro ve teknik şartları sağlayan sinyal yok.")
  print("-" * 60)


# Bot Başlatma ve Döngü
print(
    "🤖 Makro Teyitli, Hacimli & Telegram Entegreli Snaypır Botu Devrede (15 dk"
    " aralıklı)."
)

try:
  while True:
    tarama_yap()
    time.sleep(900)  # 15 Dakika (900 saniye) bekler
except KeyboardInterrupt:
  print("\nBot durduruldu.")
  
>>>>>>> 97492635f9537d9046ca7b81eab616086d3d9621
