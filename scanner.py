import time
import requests
from datetime import datetime, timezone

TOKEN = "your_token_bot_token"
CHAT = "your_telegram_chat_id"
INTERVAL = 4
MIN_SPREAD = 3.0
MIN_VOL_X = 1.5
STABLES = {"USDT","USDC","BUSD","DAI","TUSD","USDD","FRAX","USDP","GUSD","FDUSD"}

def alert(msg):
    try:
        requests.post(
            "https://api.telegram.org/bot" + TOKEN + "/sendMessage",
            data={"chat_id": CHAT, "text": msg},
            timeout=10
        )
    except Exception as e:
        print("Telegram error:", e)

def scan():
    coins = []
    for page in range(1, 9):
        try:
            r = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": 250,
                    "page": page,
                    "sparkline": False,
                    "price_change_percentage": "24h"
                },
                timeout=25
            )
            r.raise_for_status()
            batch = r.json()
            if not batch:
                break
            coins.extend(batch)
            print("  Page", page, "done ->", len(coins), "coins fetched")
            time.sleep(13)
        except Exception as e:
            print("  Page", page, "error:", e)
            time.sleep(15)

    if len(coins) < 10:
        print("Not enough data, skipping.")
        return

    btc = next((c for c in coins if c.get("symbol","").upper() == "BTC"), None)
    if not btc:
        return

    bp = btc.get("price_change_percentage_24h") or 0
    btc_price = btc.get("current_price", 0)

    vols = sorted([c.get("total_volume") or 0 for c in coins])
    med = vols[len(vols) // 2] if vols else 1

    elite = []
    true_s = []

    for c in coins:
        sym = c.get("symbol", "").upper()
        if sym in STABLES or sym == "BTC":
            continue
        ap = c.get("price_change_percentage_24h") or 0
        vol = c.get("total_volume") or 0
        vol_x = round(vol / med, 1) if med > 0 else 0
        sp = round(ap - bp, 2)
        if sp < MIN_SPREAD or vol_x < MIN_VOL_X:
            continue
        mc = c.get("market_cap", 0)
        if mc >= 1e9:
            mc_str = "$" + str(round(mc / 1e9, 1)) + "B"
        else:
            mc_str = "$" + str(round(mc / 1e6)) + "M"
        entry = {
            "sym": sym,
            "sp": sp,
            "ap": round(ap, 2),
            "vx": vol_x,
            "price": c.get("current_price", 0),
            "mc": mc_str
        }
        if bp <= 0:
            elite.append(entry)
        else:
            true_s.append(entry)

    elite.sort(key=lambda x: -x["sp"])
    true_s.sort(key=lambda x: -x["sp"])

    now = datetime.now(timezone.utc).strftime("%d %b %Y  %H:%M UTC")
    btc_sign = "+" if bp >= 0 else ""
    btc_dir = "UP" if bp >= 0 else "DOWN"

    if not elite and not true_s:
        alert(
            "RS SCANNER\n" + now +
            "\n\nNo signals this cycle." +
            "\nBTC " + btc_dir + " " + btc_sign + str(round(bp, 2)) + "%" +
            "\nScanned " + str(len(coins)) + " coins." +
            "\nNext scan in 4 hours."
        )
        print("No signals this cycle.")
        return

    lines = [
        "RS SCANNER ALERT",
        now,
        "",
        "BTC " + btc_dir + " " + btc_sign + str(round(bp, 2)) + "%   $" + str(btc_price),
        "Scanned: " + str(len(coins)) + " coins",
        ""
    ]

    if elite:
        lines.append("--- ELITE STRENGTH (" + str(len(elite)) + ") ---")
        lines.append("Coins rising while BTC is DOWN")
        lines.append("")
        for x in elite[:10]:
            s = "+" if x["sp"] >= 0 else ""
            lines.append(
                "FIRE " + x["sym"] +
                "\n  vs BTC  : " + s + str(x["sp"]) + "%" +
                "\n  24h     : +" + str(x["ap"]) + "%" +
                "\n  Volume  : " + str(x["vx"]) + "x surge" +
                "\n  Price   : $" + str(x["price"]) +
                "\n  MCap    : " + x["mc"] + "\n"
            )

    if true_s:
        lines.append("--- TRUE STRENGTH (" + str(len(true_s)) + ") ---")
        lines.append("Outpacing BTC on a green day")
        lines.append("")
        for x in true_s[:10]:
            s = "+" if x["sp"] >= 0 else ""
            lines.append(
                "CHECK " + x["sym"] +
                "\n  vs BTC  : " + s + str(x["sp"]) + "%" +
                "\n  24h     : +" + str(x["ap"]) + "%" +
                "\n  Volume  : " + str(x["vx"]) + "x surge" +
                "\n  Price   : $" + str(x["price"]) +
                "\n  MCap    : " + x["mc"] + "\n"
            )

    lines.append("Next scan in 4 hours.")
    msg = "\n".join(lines)
    alert(msg)
    print(msg)


print("=" * 40)
print("  RS Scanner - 2000 Coins Live")
print("=" * 40)
alert(
    "RS SCANNER IS LIVE\n\n"
    "Scanning 2000 coins every 4h\n"
    "All coins included except stables\n"
    "First scan starting now - takes 2 min"
)

while True:
    try:
        scan()
    except Exception as e:
        print("Error:", e)
        alert("Error: " + str(e))
    print("\nWaiting 4 hours...\n")
    time.sleep(INTERVAL * 3600)



