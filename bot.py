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
  
