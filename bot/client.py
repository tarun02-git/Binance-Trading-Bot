import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from bot.logging_config import logger

# Binance USDT-M Futures Testnet base URL
FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"

def get_binance_client() -> Client:
    """
    Initializes and returns an authenticated python-binance Client.
    Strictly targets the Binance Futures Testnet (USDT-M).
    """
    # 1. Load environment variables from the .env file
    load_dotenv()

    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_SECRET_KEY")

    # 2. Hard stop if credentials are not found
    if not api_key or not api_secret:
        logger.critical("API credentials missing from the .env file.")
        raise ValueError(
            "Missing Binance Testnet API credentials. "
            "Please ensure BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_SECRET_KEY are set in your .env file."
        )

    try:
        # 3. Initialize client and manually override the Futures API URL
        # testnet=True only points to Spot testnet, so we override it explicitly
        client = Client(api_key, api_secret, testnet=True)

        # ✅ Manually point to the correct Futures Testnet URL
        client.FUTURES_URL = FUTURES_TESTNET_URL + "/fapi"

        # 4. Ping the Futures testnet to verify connectivity
        client.futures_ping()

        logger.info("Successfully authenticated and connected to the Binance Futures Testnet.")

        return client

    except BinanceAPIException as e:
        logger.error(f"Binance API Authentication Failed (Code {e.code}): {e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected network or client initialization failure: {e}")
        raise