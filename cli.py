import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Import our core logic and validators
from bot.client import get_binance_client
from bot.orders import place_futures_order
from bot.validators import validate_symbol, validate_side, validate_order_type

# Initialize the Typer app and Rich console
app = typer.Typer(help="Binance Futures Testnet Trading Bot", no_args_is_help=True)
console = Console()

@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair (e.g. BTCUSDT)", callback=validate_symbol),
    side: str = typer.Option(..., "--side", "-d", help="BUY or SELL", callback=validate_side),
    order_type: str = typer.Option(..., "--type", "-t", help="MARKET, LIMIT, STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET", callback=validate_order_type),
    quantity: float = typer.Option(..., "--qty", "-q", help="Amount to trade in base asset"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Limit execution price (Required for LIMIT/STOP/TAKE_PROFIT)"),
    stop_price: Optional[float] = typer.Option(None, "--stop", "-sp", help="Trigger price (Required for STOP/TAKE_PROFIT/STOP_MARKET/TAKE_PROFIT_MARKET)")
):
    """
    Executes a trade on the Binance Futures Testnet.
    """
    # 1. UI: Display Execution Intent Panel
    intent_text = (
        f"Symbol: [bold yellow]{symbol}[/bold yellow] | Side: [bold yellow]{side}[/bold yellow] | Type: [bold yellow]{order_type}[/bold yellow]\n"
        f"Quantity: {quantity} | Price: {price} | Stop Trigger: {stop_price}"
    )
    console.print(Panel(intent_text, title="[bold cyan]Transmitting Order Request[/bold cyan]", border_style="cyan"))

    # 2. Cross-Parameter Validation
    if order_type in ["LIMIT", "STOP", "TAKE_PROFIT"] and price is None:
        console.print("[bold red]Fatal Error:[/bold red] The --price parameter is mandatory for LIMIT, STOP and TAKE_PROFIT orders.")
        raise typer.Exit(code=1)

    if order_type in ["STOP", "TAKE_PROFIT", "STOP_MARKET", "TAKE_PROFIT_MARKET"] and stop_price is None:
        console.print("[bold red]Fatal Error:[/bold red] The --stop parameter is mandatory for STOP, TAKE_PROFIT, STOP_MARKET and TAKE_PROFIT_MARKET orders.")
        raise typer.Exit(code=1)

    try:
        # 3. Connect & Execute
        with console.status("[bold green]Contacting Binance Testnet matching engine...", spinner="dots"):
            client = get_binance_client()
            response = place_futures_order(
                client=client,
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )

        # 4. UI: Build and Display the Success Table
        table = Table(title="Execution Response Metrics", show_header=True, header_style="bold green")
        table.add_column("Exchange Metric", style="cyan", justify="right")
        table.add_column("Reported Value", style="magenta")

        # ✅ Check both orderId and algoId (STOP orders use algoId)
        order_id = response.get("orderId") or response.get("algoId", "N/A")
        table.add_row("Order ID", str(order_id))

        # ✅ Check both status and algoStatus (STOP orders use algoStatus)
        status = response.get("status") or response.get("algoStatus", "N/A")
        table.add_row("Execution Status", str(status))

        table.add_row("Trading Pair", str(response.get("symbol", "N/A")))
        table.add_row("Direction", str(response.get("side", "N/A")))

        # ✅ Check both type and orderType (STOP orders use orderType)
        order_type_resp = response.get("type") or response.get("orderType", "N/A")
        table.add_row("Order Type", str(order_type_resp))

        table.add_row("Executed Quantity", str(response.get("executedQty", response.get("quantity", "0.0"))))

        # Capture blended fill price if available, otherwise fallback to target price
        avg_price = response.get("avgPrice") or response.get("price", "N/A")
        table.add_row("Average Fill Price", str(avg_price))

        # ✅ Show stop trigger price if present (STOP orders)
        if response.get("stopPrice") or response.get("triggerPrice"):
            trigger = response.get("stopPrice") or response.get("triggerPrice")
            table.add_row("Stop Trigger Price", str(trigger))

        console.print(table)
        console.print(f"[bold green]✓ SEQUENCE COMPLETE:[/bold green] Order for {symbol} processed successfully.")

    except Exception as e:
        console.print(f"[bold red]✗ SEQUENCE HALTED:[/bold red] Order execution failed.")
        console.print(f"[red]Diagnostic Reason:[/red] {str(e)}")
        console.print("Please check your [bold]bot.log[/bold] file for full network payloads and tracebacks.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()