import pandas as pd
import time
import requests
from telegram import Bot

# 🛠️ اطلاعات توکن و چت آیدی تلگرام
TELEGRAM_TOKEN = '7590231828:AAHmp8UIirv_Hb_pTHc-TGvqZWtu4xd7cPo'
TELEGRAM_CHAT_ID = '749823138'

# 🛠️ لیست نمادها
symbols = {
    'BTCIRT': 'BTC-IRT',
    'SOLIRT': 'SOL-IRT',
    'LOFIIRT': 'LOFI-IRT'
}

# 🛠️ ساخت بات تلگرام
bot = Bot(token=TELEGRAM_TOKEN)

# 🛠️ دریافت داده کندل‌ها از رمزینکس
def get_ohlcv(symbol):
    url = f"https://api.ramzinex.com/exchange/api/v1/market/candles/{symbol}?resolution=5m&limit=100"
    response = requests.get(url)
    data = response.json()['result']
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['close'] = df['close'].astype(float)
    return df

# 🛠️ محاسبه RSI
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# 🛠️ بررسی سیگنال خرید و فروش
def check_signal(df, symbol_name):
    close = df['close']
    last_close = close.iloc[-1]

    # محاسبه RSI
    rsi = compute_rsi(close)
    last_rsi = rsi.iloc[-1]

    # محاسبه Bollinger Bands
    ma = close.rolling(window=20).mean()
    std = close.rolling(window=20).std()
    upper_band = ma + (2 * std)
    lower_band = ma - (2 * std)

    last_upper = upper_band.iloc[-1]
    last_lower = lower_band.iloc[-1]

    # 🚨 هشدار خرید
    if last_close < last_lower and last_rsi < 30:
        msg = f"🔥 سیگنال خرید در {symbol_name}\nقیمت: {last_close:.2f}\nRSI: {last_rsi:.2f}"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

    # 🚨 هشدار فروش
    if last_close > last_upper and last_rsi > 70:
        msg = f"⚠️ سیگنال فروش در {symbol_name}\nقیمت: {last_close:.2f}\nRSI: {last_rsi:.2f}"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

# 🔁 حلقه اصلی
while True:
    try:
        for symbol, symbol_name in symbols.items():
            df = get_ohlcv(symbol)
            check_signal(df, symbol_name)
            print(f"✅ بررسی {symbol_name} انجام شد.")
    except Exception as e:
        print(f"❌ خطا: {e}")

    time.sleep(300)  # Sleep for 5 minutes
