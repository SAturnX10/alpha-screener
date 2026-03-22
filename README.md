# Crypto Relative Strength Scanner

A free, open-source Python tool that scans the **top 2000 cryptocurrencies** 
every 4 hours, finds coins showing real strength compared to BTC, and sends 
alerts directly to your **Telegram**.

Zero cost. No paid APIs. Runs on any PC or free cloud server.

---

## What it does

- Scans 2000 coins from CoinGecko every 4 hours (free API, no key needed)
- Compares every coin's 24h price change against BTC
- Filters out stablecoins automatically
- Tags signals as ELITE or TRUE strength
- Sends clean Telegram alerts only when real signals appear — no noise

## Signal types

**ELITE** — coin is rising while BTC is flat or down. Rarest and most 
powerful signal. Real money flowing in regardless of the market.

**TRUE** — coin is outpacing BTC on a green day. Strong but less rare.

## Example Telegram alert
```
RS SCANNER ALERT
23 Mar 2026  14:00 UTC

BTC DOWN -1.20%   $83,400
Scanned: 2000 coins

--- ELITE STRENGTH (2) ---
Coins rising while BTC is DOWN

FIRE SOL
  vs BTC  : +5.80%
  24h     : +4.60%
  Volume  : 3.2x surge
  Price   : $142.5
  MCap    : $62.1B
```

## Setup

**1. Install Python**
Download from python.org. Tick "Add to PATH" during install.

**2. Install the library**
```
python -m pip install requests
```

**3. Configure your Telegram bot**

- Message @BotFather on Telegram → /newbot → copy your token
- Message @userinfobot → copy your ID
- Edit scanner.py and fill in:
```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT  = "YOUR_TELEGRAM_CHAT_ID"
```

**4. Run it**
```
python scanner.py
```

## Settings you can change

| Setting | Default | What it does |
|---|---|---|
| MIN_SPREAD | 3.0 | Minimum % a coin must beat BTC by |
| MIN_VOL_X | 1.5 | Minimum volume surge multiplier |
| INTERVAL | 4 | Hours between each scan |

## Requirements

- Python 3.8+
- requests library
- Free CoinGecko API (no key needed)
- Telegram bot (free)

## Disclaimer

This tool is for informational purposes only. Not financial advice. 
Always do your own research before making any trading decisions.

---

If this helped you, please star the repo.
