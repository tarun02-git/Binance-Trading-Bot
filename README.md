# 🤖 Binance Futures Testnet Trading Bot

A professional, command-line trading bot built in Python that executes trades on the **Binance USDT-M Futures Testnet**. Supports Market, Limit, Stop, and Take Profit orders with automatic price/quantity precision formatting and a rich terminal UI.

> ⚠️ **This bot operates exclusively on the Binance Futures Testnet — no real money is involved.**

---

## 📸 Preview

```
╭─────────────────── Transmitting Order Request ───────────────────╮
│ Symbol: BTCUSDT | Side: BUY | Type: MARKET                       │
│ Quantity: 0.05 | Price: None | Stop Trigger: None                │
╰──────────────────────────────────────────────────────────────────╯

         Execution Response Metrics
┌──────────────────────┬──────────────────────┐
│        Exchange Metric │ Reported Value       │
├──────────────────────┼──────────────────────┤
│               Order ID │ 123456789            │
│      Execution Status  │ FILLED               │
│           Trading Pair │ BTCUSDT              │
│             Direction  │ BUY                  │
│             Order Type │ MARKET               │
│      Executed Quantity │ 0.050                │
│     Average Fill Price │ 84321.50             │
└──────────────────────┴──────────────────────┘

✓ SEQUENCE COMPLETE: Order for BTCUSDT processed successfully.
```

---

## ✨ Features

- ✅ **Market Orders** — Instant execution at best available price
- ✅ **Limit Orders** — Execute only at your specified price
- ✅ **Stop Orders** — Automatic stop-loss with limit price trigger
- ✅ **Take Profit Orders** — Lock in gains at a target price
- ✅ **Stop Market / Take Profit Market** — Trigger-based market execution
- ✅ **Auto Precision Formatting** — Automatically rounds price & quantity to exchange rules
- ✅ **Rich Terminal UI** — Color-coded panels and tables via the `rich` library
- ✅ **Dual Logging** — Console + persistent `bot.log` file
- ✅ **Input Validation** — Catches invalid symbols, sides, and order types before sending

---

## 🗂️ Project Structure

```
binance_testnet_bot/
├── bot/
│   ├── client.py          # Authenticates and connects to Binance Futures Testnet
│   ├── orders.py          # Core order placement logic (all order types)
│   ├── validators.py      # CLI input validation callbacks
│   └── logging_config.py  # Dual console + file logging setup
├── .env                   # API credentials (never commit this!)
├── .gitignore             # Excludes .env, venv, logs from git
├── bot.log                # Auto-generated trade log
├── cli.py                 # Main CLI entry point
└── requirements.txt       # Python dependencies
```

---

## ⚙️ Prerequisites

- Python 3.12+
- A [GitHub](https://github.com) account
- A [Binance Futures Testnet](https://testnet.binancefuture.com) account

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/binance-testnet-bot.git
cd binance-testnet-bot
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your Futures Testnet API keys

1. Go to 👉 [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Click **"Log in with GitHub"**
3. Scroll down to the **API Key** section
4. Click **"Generate Key"**
5. Copy both the **API Key** and **Secret Key**

> ⚠️ **Important:** These are Futures Testnet keys — they are completely separate from your real Binance account keys and from the Spot Testnet keys at `testnet.binance.vision`.

### 5. Configure your `.env` file

Create a `.env` file in the project root:

```env
BINANCE_TESTNET_API_KEY=your_api_key_here
BINANCE_TESTNET_SECRET_KEY=your_secret_key_here
```

> ⚠️ Never add spaces around the `=` sign and never commit this file to GitHub.

---

## 💻 Usage

All commands follow this structure:

```bash
python cli.py --symbol <SYMBOL> --side <SIDE> --type <ORDER_TYPE> --qty <QUANTITY> [--price <PRICE>] [--stop <STOP_PRICE>]
```

### Options

| Flag | Short | Description | Required |
|------|-------|-------------|----------|
| `--symbol` | `-s` | Trading pair e.g. `BTCUSDT` | ✅ Always |
| `--side` | `-d` | `BUY` or `SELL` | ✅ Always |
| `--type` | `-t` | Order type (see below) | ✅ Always |
| `--qty` | `-q` | Quantity in base asset | ✅ Always |
| `--price` | `-p` | Limit execution price | ⚠️ LIMIT, STOP, TAKE_PROFIT |
| `--stop` | `-sp` | Stop trigger price | ⚠️ STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET |

---

## 📋 Order Type Examples

### Market Order
Executes immediately at the best available price.
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.05
```

### Limit Order
Executes only when the market reaches your specified price.
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.05 --price 60000
```

### Stop Order (Stop Loss)
Places a limit sell order when the market drops to your trigger price.
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP --qty 0.05 --price 59900 --stop 60000
```

### Stop Market Order
Places a market sell order when the trigger price is hit.
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.05 --stop 60000
```

### Take Profit Order
Places a limit sell order when the market rises to your trigger price.
```bash
python cli.py --symbol BTCUSDT --side SELL --type TAKE_PROFIT --qty 0.05 --price 95000 --stop 94000
```

### Take Profit Market Order
Places a market sell order when the take profit trigger is hit.
```bash
python cli.py --symbol BTCUSDT --side SELL --type TAKE_PROFIT_MARKET --qty 0.05 --stop 94000
```

---

## 🔍 Verifying Orders on the Testnet

After placing an order, verify it at [https://testnet.binancefuture.com](https://testnet.binancefuture.com):

| Order Type | Where to Find It |
|------------|-----------------|
| MARKET, LIMIT | **Orders → Open Orders → Basic** tab |
| STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET | **Orders → Open Orders → Conditional** tab |

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `python-binance` | Binance API wrapper |
| `python-dotenv` | Load credentials from `.env` file |
| `typer[all]` | CLI framework |
| `rich` | Terminal UI (panels, tables, colors) |

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🛡️ Security Notes

- Never commit your `.env` file — it is excluded via `.gitignore`
- Never use real Binance API keys with this bot
- Always use keys from [testnet.binancefuture.com](https://testnet.binancefuture.com) only
- Testnet keys expire periodically — regenerate them if you get a `-2015` error

---

## 📝 Logging

All activity is logged in two places simultaneously:

- **Terminal** — Color-coded output via `rich`
- **`bot.log`** — Persistent file log with timestamps, useful for debugging

```
2026-03-26 11:05:08 - BinanceTestnetBot - INFO - Successfully authenticated and connected to the Binance Futures Testnet.
2026-03-26 11:05:09 - BinanceTestnetBot - DEBUG - Transmitting finalized order payload: {'symbol': 'BTCUSDT', ...}
2026-03-26 11:05:10 - BinanceTestnetBot - INFO - Order transmitted and accepted! Order ID: 123456789
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — feel free to use, modify, and distribute it.

---

## ⚠️ Disclaimer

This bot is built for **educational purposes** on the Binance Futures Testnet only. It does not constitute financial advice. Always do your own research before trading with real funds. The authors are not responsible for any financial losses.
