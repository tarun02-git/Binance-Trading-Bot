from decimal import Decimal, ROUND_DOWN
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from bot.logging_config import logger

def get_symbol_filters(client: Client, symbol: str) -> tuple[float, float]:
    """
    Queries the exchange to dynamically acquire the PRICE_FILTER (tickSize) 
    and LOT_SIZE (stepSize) constraints for the specified symbol.
    """
    try:
        logger.debug(f"Requesting exchange filter rules for {symbol}...")
        
        exchange_info = client.futures_exchange_info()
        
        tick_size = None
        step_size = None
        
        for symbol_info in exchange_info['symbols']:
            if symbol_info['symbol'] == symbol:
                
                for filter_rule in symbol_info['filters']:
                    if filter_rule['filterType'] == 'PRICE_FILTER':
                        tick_size = float(filter_rule['tickSize'])
                    elif filter_rule['filterType'] == 'LOT_SIZE':
                        step_size = float(filter_rule['stepSize'])
                
                if tick_size and step_size:
                    logger.debug(f"Extracted rules for {symbol}: tickSize={tick_size}, stepSize={step_size}")
                    return tick_size, step_size
                
        raise ValueError(f"Symbol {symbol} not found on the exchange, or missing critical filters.")
    
    except Exception as e:
        logger.error(f"Failed to fetch exchange filters: {e}")
        raise


def round_step_size(raw_value: float, step_size: float) -> float:
    """
    Rounds a given quantity or price strictly down to the exchange's required step_size.
    Utilizes the Decimal module to circumvent floating-point drift.
    """
    value_dec = Decimal(str(raw_value))
    step_dec = Decimal(str(step_size))
    
    rounded_value = value_dec - (value_dec % step_dec)
    final_value = rounded_value.quantize(step_dec, rounding=ROUND_DOWN)
    
    return float(final_value)


def place_futures_order(
    client: Client, 
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    price: float = None,
    stop_price: float = None
) -> dict:
    """
    Constructs the API payload and transmits a Market, Limit, or Stop order.
    Automates the dynamic precision scaling to prevent filter rejections.

    Supported order types:
        - MARKET           : Fill immediately at best available price
        - LIMIT            : Fill at your specific price
        - STOP             : Stop loss with a limit price (requires stop_price + price)
        - TAKE_PROFIT      : Take profit with a limit price (requires stop_price + price)
        - STOP_MARKET      : Stop loss at market price (requires stop_price only)
        - TAKE_PROFIT_MARKET: Take profit at market price (requires stop_price only)
    """
    try:
        # 1. Fetch live precision rules from the exchange
        tick_size, step_size = get_symbol_filters(client, symbol)
        
        # 2. Format the quantity mathematically down to the strict LOT_SIZE
        formatted_qty = round_step_size(quantity, step_size)
        
        if formatted_qty <= 0:
            raise ValueError(f"Truncated quantity is {formatted_qty}. It must exceed the step size ({step_size}).")

        # 3. Construct the base payload required for ALL orders
        payload = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": formatted_qty
        }

        # 4. Append price + timeInForce for all limit-based order types
        # STOP and TAKE_PROFIT are the correct Binance Futures names (not STOP_LOSS_LIMIT)
        if order_type.upper() in ["LIMIT", "STOP", "TAKE_PROFIT"]:
            if price is None:
                raise ValueError(f"A target price parameter is mandatory for {order_type.upper()} orders.")
            
            # Format the target limit price strictly down to the PRICE_FILTER tick size
            payload["price"] = round_step_size(price, tick_size)
            
            # GTC (Good-Til-Canceled) is mandatory for limit-based orders on Binance Futures
            payload["timeInForce"] = "GTC"

        # 5. Append stopPrice trigger for STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET
        if order_type.upper() in ["STOP", "TAKE_PROFIT", "STOP_MARKET", "TAKE_PROFIT_MARKET"]:
            if stop_price is None:
                raise ValueError(f"A stop_price trigger parameter is mandatory for {order_type.upper()} orders.")
            
            # Format the conditional trigger price to match PRICE_FILTER rules
            payload["stopPrice"] = round_step_size(stop_price, tick_size)

        # 6. Warn if price is accidentally passed for a MARKET order
        if order_type.upper() == "MARKET" and price is not None:
            logger.warning(f"Price parameter ({price}) was provided but will be ignored for MARKET orders.")

        # Log the exact payload before it leaves our server
        logger.debug(f"Transmitting finalized order payload: {payload}")

        # 7. Execute the HTTP POST request via the python-binance wrapper
        response = client.futures_create_order(**payload)
        
        logger.info(f"Order transmitted and accepted! Order ID: {response.get('orderId') or response.get('algoId')}")
        
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Rejection (Status {e.status_code}, Code {e.code}): {e.message}")
        raise
    except Exception as e:
        logger.error(f"Critical error during order placement sequence: {e}")
        raise