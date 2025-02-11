import MetaTrader5 as mt5
import time

def connect_to_mt5():
    # Ask for broker, username, and password
    broker = input("Enter Broker Name: ")
    username = int(input("Enter Username (as number): "))
    password = input("Enter Password: ")

    # Initialize MT5
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        print("Ensure MT5 is installed and the path is correct.")
        quit()
    else:
        print("MT5 initialized successfully")

    # Login to the account
    authorized = mt5.login(username, password, server=broker)
    if authorized:
        print("Logged in to account #{}".format(username))
    else:
        print("Failed to login, error code =", mt5.last_error())
        mt5.shutdown()
        quit()

def get_account_info():
    account_info = mt5.account_info()
    if account_info:
        print("Account Info:")
        print("  Balance:", account_info.balance)
        print("  Equity:", account_info.equity)
        print("  Margin:", account_info.margin)
        print("  Leverage:", account_info.leverage)
    else:
        print("Failed to retrieve account info, error code =", mt5.last_error())

def check_symbol(symbol):
    # Check if the symbol is available in MarketWatch
    selected = mt5.symbol_select(symbol, True)
    if not selected:
        print("Failed to select symbol:", symbol)
    else:
        print("Symbol", symbol, "selected successfully.")

def get_symbol_data(symbol, timeframe=mt5.TIMEFRAME_M1, bars=10):
    # Request historical data for the symbol
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None:
        print("Failed to get rates for", symbol, "error code =", mt5.last_error())
        return None
    else:
        print("Recent", bars, "bars for", symbol, ":")
        for rate in rates:
            print(rate)
        return rates

def place_order(symbol, order_type, volume, price, sl=0.0, tp=0.0, deviation=20):
    # Prepare the request structure
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print("Symbol not found, cannot place order")
        return

    point = symbol_info.point
    # Create the order request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": sl if sl > 0.0 else price - 100 * point,  # example stop-loss
        "tp": tp if tp > 0.0 else price + 100 * point,   # example take-profit
        "deviation": deviation,
        "magic": 234000,  # your EA magic number
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,  # Good till canceled
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # Send the order request
    result = mt5.order_send(request)
    print("Order send result:", result)
    return result

def main():
    # Connect to MT5
    connect_to_mt5()

    # Get and display account information
    get_account_info()

    # Choose a symbol to work with (e.g., "EURUSD")
    symbol = "EURUSD"
    check_symbol(symbol)

    # Fetch and display recent market data
    rates = get_symbol_data(symbol, mt5.TIMEFRAME_M1, 10)

    # Example: Place a sample BUY order if desired.
    # Note: Use this with caution and preferably in a demo account first.
    if rates:
        current_price = rates[-1]['close']
        print("Current price for", symbol, "is", current_price)
        # Uncomment the next line to place a buy order
        # result = place_order(symbol, mt5.ORDER_TYPE_BUY, volume=0.01, price=current_price)
    
    # Keep the connection alive for a bit if needed for further testing
    time.sleep(2)

    # Shutdown MT5 connection
    mt5.shutdown()
    print("MT5 connection closed")

if __name__ == "__main__":
    main()
