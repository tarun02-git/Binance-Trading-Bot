import typer

def validate_symbol(ctx: typer.Context, value: str) -> str:
    """Ensures the trading pair is purely alphanumeric and uppercase."""
    # Skip validation if Typer is running a shell auto-completion check
    if ctx.resilient_parsing:
        return value
        
    if not value.isalnum():
        raise typer.BadParameter("Symbol must be purely alphanumeric (e.g., BTCUSDT).")
    
    return value.upper()


def validate_side(ctx: typer.Context, value: str) -> str:
    """Ensures the order side is strictly constrained to BUY or SELL."""
    if ctx.resilient_parsing:
        return value
        
    side = value.upper()
    if side not in ["BUY", "SELL"]:  # ✅ Fixed: added the valid values list
        raise typer.BadParameter("Side must be either 'BUY' or 'SELL'.")
        
    return side


def validate_order_type(ctx: typer.Context, value: str) -> str:
    """Restricts the order types to our supported implementation subset."""
    if ctx.resilient_parsing:
        return value
        
    order_type = value.upper()
    valid_types = ["MARKET", "LIMIT", "STOP", "TAKE_PROFIT", "STOP_MARKET", "TAKE_PROFIT_MARKET"]  # ✅ Fixed: added the valid types list
    
    if order_type not in valid_types:
        raise typer.BadParameter(f"Order type must be one of: {', '.join(valid_types)}")
        
    return order_type