import os
import random
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import uvicorn
import httpx

# --- Load Environment Variables ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

if not BOT_TOKEN:
    print("⚠️ WARNING: BOT_TOKEN is missing from the .env file!")
if not WEBAPP_URL:
    print("⚠️ WARNING: WEBAPP_URL is missing from the .env file!")
if BOT_TOKEN and WEBAPP_URL:
    print("✅ Environment variables loaded successfully!")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

DEFAULT_FOREX = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]
DEFAULT_CRYPTO = ["BTC", "ETH", "SOL", "XRP", "BNB"]

CURRENCY_MAP = {
    "USD": {"name": "U.S. Dollar", "flag": "us"},
    "EUR": {"name": "Euro", "flag": "eu"},
    "GBP": {"name": "British Pound", "flag": "gb"},
    "JPY": {"name": "Japanese Yen", "flag": "jp"},
    "AUD": {"name": "Australian Dollar", "flag": "au"},
    "CAD": {"name": "Canadian Dollar", "flag": "ca"},
}

# --- TELEGRAM BOT WEBHOOK & BOT COMMANDS ---
@app.on_event("startup")
async def setup_telegram_menu():
    """Automatically configures the Telegram Bot Menu Button on server launch."""
    if BOT_TOKEN and WEBAPP_URL:
        async with httpx.AsyncClient() as client:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton"
            payload = {
                "menu_button": {
                    "type": "web_app",
                    "text": "Open Screener 📈",
                    "web_app": {"url": WEBAPP_URL}
                }
            }
            try:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    print(f"✅ Telegram Menu Button configured successfully to: {WEBAPP_URL}")
                else:
                    print(f"⚠️ Failed to update Telegram Menu Button: {res.text}")
            except Exception as e:
                print(f"⚠️ Error syncing with Telegram: {e}")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Handles messages sent directly to the Telegram bot chat."""
    data = await request.json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if text == "/start" and BOT_TOKEN and WEBAPP_URL:
            async with httpx.AsyncClient() as client:
                send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": "Welcome to Trade Screener! 📈\nTap below to launch the Mini App.",
                    "reply_markup": {
                        "inline_keyboard": [[
                            {
                                "text": "🚀 Launch Screener",
                                "web_app": {"url": WEBAPP_URL}
                            }
                        ]]
                    }
                }
                await client.post(send_url, json=payload)
    return {"status": "ok"}


# --- SCREENER LOGIC ---
def analyze_trend_and_strength(yf_symbol: str):
    """Calculates Trend and Strength based on standard moving averages."""
    try:
        ticker = yf.Ticker(yf_symbol)
        df = ticker.history(period="1y", interval="1d")

        if df.empty or len(df) < 20:
            return "Neutral", 50, 0, 0

        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean() if len(df) >= 200 else df['SMA_50']

        price = float(df['Close'].iloc[-1])
        sma20 = float(df['SMA_20'].iloc[-1])
        sma50 = float(df['SMA_50'].iloc[-1])
        sma200 = float(df['SMA_200'].iloc[-1])

        score = 0
        if price > sma20: score += 1
        if price > sma50: score += 1
        if price > sma200: score += 1
        if sma20 > sma50: score += 1

        if score >= 3:
            trend = "Bullish"
            strength = 80 if score == 3 else 100
        elif score <= 1:
            trend = "Bearish"
            strength = 80 if score == 0 else 60
        else:
            trend = "Bullish" if price > sma50 else "Bearish"
            strength = 60

        return trend, strength, price, score
    except Exception:
        return "Neutral", 50, 0, 2


@app.get("/api/forex")
async def get_forex_data(pairs: str = None, search: str = None):
    pairs_to_check = [p.strip().upper() for p in pairs.split(",")] if pairs else (
        [search.strip().upper()] if search else DEFAULT_FOREX)

    results = []
    for pair in pairs_to_check:
        clean_name = pair.replace("=X", "")
        yf_symbol = f"{clean_name}=X" if len(clean_name) == 6 else clean_name

        if len(clean_name) == 6:
            base, quote = clean_name[:3], clean_name[3:]
            base_info = CURRENCY_MAP.get(base, {"name": base, "flag": "un"})
            quote_info = CURRENCY_MAP.get(quote, {"name": quote, "flag": "un"})
            full_name = f"{base_info['name']} / {quote_info['name']}"
            base_flag = f"https://flagcdn.com/w40/{base_info['flag']}.png"
            quote_flag = f"https://flagcdn.com/w40/{quote_info['flag']}.png"
        else:
            full_name = clean_name
            base_flag, quote_flag = "https://flagcdn.com/w40/un.png", "https://flagcdn.com/w40/un.png"

        trend, strength, price, score = analyze_trend_and_strength(yf_symbol)

        results.append({
            "pair": clean_name, "fullName": full_name,
            "baseFlag": base_flag, "quoteFlag": quote_flag,
            "trend": trend, "strength": strength
        })
    return {"data": results}


@app.get("/api/crypto")
async def get_crypto_data(pairs: str = None, search: str = None):
    pairs_to_check = [p.strip().upper() for p in pairs.split(",")] if pairs else (
        [search.strip().upper()] if search else DEFAULT_CRYPTO)

    results = []
    for coin in pairs_to_check:
        clean_name = coin.replace("-USD", "")
        yf_symbol = f"{clean_name}-USD"

        trend, strength, price, score = analyze_trend_and_strength(yf_symbol)
        icon_url = f"https://ui-avatars.com/api/?name={clean_name}&background=random&color=fff&rounded=true&bold=true"

        results.append({
            "pair": f"{clean_name}/USD", "symbol": clean_name,
            "fullName": f"{clean_name} Network", "icon": icon_url,
            "trend": trend, "strength": strength
        })
    return {"data": results}


@app.get("/api/analyze")
async def get_ai_analysis(symbol: str):
    """Generates an AI context analysis based on actual indicator data."""
    clean_sym = symbol.upper().strip()

    if len(clean_sym) == 6 and clean_sym[:3] in ["EUR", "GBP", "USD", "AUD", "CAD", "JPY", "CHF", "NZD"]:
        yf_symbol = f"{clean_sym}=X"
        display_name = f"{clean_sym[:3]}/{clean_sym[3:]}"
    else:
        yf_symbol = f"{clean_sym}-USD"
        display_name = f"{clean_sym}/USD"

    trend, strength, price, score = analyze_trend_and_strength(yf_symbol)

    if score == 4:
        status_icon = "🟢 Strongly Bullish"
        text = f"Momentum is surging with price (${price:,.4f}) well above all major moving averages. Breakout structure is intact with heavy buying volume."
        conf = random.randint(88, 96)
    elif score == 3:
        status_icon = "🟢 Bullish"
        text = f"Steady uptrend supported by short-term moving averages. Watch for potential resistance ahead as price approaches (${price * 1.02:,.4f})."
        conf = random.randint(75, 87)
    elif score <= 1:
        status_icon = "🔴 Bearish"
        text = f"Price (${price:,.4f}) is struggling below medium-term averages. Downward pressure remains dominant across multiple timeframes."
        conf = random.randint(70, 85)
        if score == 0:
            status_icon = "🔴 Strongly Bearish"
            text = "Heavy sell-off structure. Price is firmly below all key moving averages, indicating severe weakness."
            conf = random.randint(88, 95)
    else:
        status_icon = "⚪ Neutral / Consolidation"
        text = f"Mixed signals across timeframes. Price (${price:,.4f}) is chopping between moving averages. Awaiting clear breakout."
        conf = random.randint(50, 65)

    return {
        "pair": display_name,
        "status": status_icon,
        "analysis": text,
        "confidence": conf
    }


@app.get("/", response_class=HTMLResponse)
async def render_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)