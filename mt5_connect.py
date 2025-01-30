import MetaTrader5 as mt5

def connect_to_mt5():
    # Ask for broker, username, and password
    broker = input("Enter Broker Name: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    # Initialize MT5
    if not mt5.initialize():
        print("Initialize() failed, error code =", mt5.last_error())
        print("Ensure MT5 is installed and the path is correct.")
        quit()
    else:
        print("MT5 initialized successfully")

    # Login to the account
    authorized = mt5.login(username, password, broker)
    if authorized:
        print("Logged in to account #{}".format(username))
    else:
        print("Failed to login, error code =", mt5.last_error())
        mt5.shutdown()
        quit()

def main():
    # Connect to MT5
    connect_to_mt5()

    # Shutdown MT5 connection
    mt5.shutdown()
    print("MT5 connection closed")

if __name__ == "__main__":
    main()
