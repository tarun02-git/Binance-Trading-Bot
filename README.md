Binance Futures Testnet Trading Bot 🤖📈
A robust, enterprise-grade command-line trading application built in Python. This bot is engineered to execute algorithmic trades safely on the Binance Futures Testnet (USDT-M) utilizing the official python-binance wrapper.

By isolating business logic from the presentation layer and utilizing exact base-10 mathematics, this project guarantees strict adherence to exchange filters while providing a beautiful, colorized terminal user experience.

🌟 Key Features
Zero Financial Risk: Exclusively targets the https://testnet.binancefuture.com infrastructure, ensuring all executions utilize simulated testnet tokens with no actual monetary value.

Advanced Order Typology: Supports immediate liquidity extraction (MARKET), liquidity provisioning (LIMIT), and dormant conditional triggers (STOP_LOSS_LIMIT).

Deterministic Precision: Automatically queries the exchange for dynamic PRICE_FILTER and LOT_SIZE rules, using the decimal module to format inputs and eliminate the notorious APIError(code=-1013): Filter failure rejections.

Dual-Channel Telemetry: Avoids the standard Python root logger to prevent noise. It implements a terminal-friendly standard output alongside a silent RotatingFileHandler that persistently archives granular payloads and tracebacks without consuming excessive disk space.

Resilient CLI UX: Built on typer and rich, featuring automated parameter validation, Tab-completion safety, and dynamic color-coded execution tables.

🏗️ Project Architecture
binance_testnet_bot/
├── bot/
│   ├── init.py

│   ├── client.py             # Network connection & Testnet authentication
│   ├── orders.py             # Order execution & mathematical formatting
│   ├── validators.py         # Typer CLI input sanitization callbacks
│   └── logging_config.py     # Dual-handler RotatingFile logger
├── cli.py                    # Typer/Rich command-line entry point
├── requirements.txt          # Explicit dependency mapping
├──.env                      # Local cryptographic credentials (Git-ignored)
└── README.md

⚙️ Prerequisites & Setup
Python Installation: Ensure you have Python 3.8 or higher installed on your system.

Account Provisioning: Register for a simulated account at the(https://testnet.binancefuture.com).

Generate API Keys: Navigate to the API Management section to generate your system-generated HMAC API Key and Secret Key.

Security Best Practices 🔐
Never commit your API keys to version control. It is highly recommended to restrict your API key access to your trusted IP address and ensure that withdrawal permissions are strictly disabled.

🚀 Installation
1. Clone the repository and navigate into the directory:

Bash
git clone https://github.com/YourUsername/Binance-Futures-Testnet-Bot.git
cd Binance-Futures-Testnet-Bot
2. Create and activate a Python virtual environment:

Bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
3. Install dependencies:

Bash
pip install -r requirements.txt
4. Configure Environment Variables:
Create a .env file in the root directory and add your Testnet credentials:

Code snippet
BINANCE_TESTNET_API_KEY=your_testnet_api_key_here
BINANCE_TESTNET_SECRET_KEY=your_testnet_secret_key_here
💻 Usage & Commands
The application is triggered via the cli.py entry point. The system automatically fetches exchange filters and handles all fractional precision formatting (tickSize and stepSize) prior to network transmission.

1. Market Order (Immediate Execution)
Consumes existing order book liquidity immediately.

Bash
python cli.py trade --symbol BTCUSDT --side BUY --type MARKET --qty 0.05
2. Limit Order (Delayed Execution)
Provides liquidity to the order book at a specific price threshold. Requires the --price (-p) parameter.

Bash
python cli.py trade --symbol ETHUSDT --side SELL --type LIMIT --qty 1.5 --price 3500.50
3. Stop-Loss-Limit Order (Conditional Risk Management)
Injects a dormant trigger that executes a Limit order upon the market crossing a specific price point. Requires both --price (the limit execution price) and --stop (the conditional trigger threshold).

Bash
python cli.py trade --symbol SOLUSDT --side SELL --type STOP_LOSS_LIMIT --qty 10 --price 140 --stop 145
📊 Monitoring & Logs
The bot will print a beautiful, colorized summary of successful executions directly to your terminal. However, detailed network telemetry, API responses, and exception tracebacks are silently routed to the bot.log file in your root directory.

If an order fails, check this file to view the exact JSON payload that was transmitted to Binance and the specific HTTP error code returned.
