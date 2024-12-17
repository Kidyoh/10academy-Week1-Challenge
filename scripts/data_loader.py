import pandas as pd
import yfinance as yf

def load_news_data(file_path):
    df = pd.read_csv(file_path)
 # Convert date column to datetime with error handling
    try:
        df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
        print(f"Successfully converted {df['date'].notna().sum()} dates")
        print(f"Failed to convert {df['date'].isna().sum()} dates")
    except Exception as e:
        print(f"Error converting dates: {str(e)}")
        print("Sample of date values:")
        print(df['date'].head())
    
    return df

def load_stock_data(symbol, start_date, end_date):
    """Fetch stock data for a given symbol and date range."""
    stock = yf.Ticker(symbol)
    df = stock.history(start=start_date, end=end_date)
    df.index = df.index.tz_localize(None)  # Remove timezone info for easier merging
    return df

def merge_data(news_df, stock_df):
    """Merge news and stock data based on date."""
    return pd.merge(news_df, stock_df, left_on='date', right_index=True, how='inner')

