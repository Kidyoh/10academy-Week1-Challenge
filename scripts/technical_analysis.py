import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from ta.trend import sma_indicator, ema_indicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.volume import on_balance_volume

def load_stock_data(symbol, start_date, end_date):
    """
    Load stock data from local CSV files
    """
    try:
        # Adjust the path according to your file structure
        file_path = f'data/yfinance_data/{symbol}_historical_data.csv'
        df = pd.read_csv(file_path)
        
        # Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        
        # Filter by date range if needed
        df = df[(df.index >= start_date) & (df.index <= end_date)]
        
        print(f"Successfully loaded data for {symbol}")
        return df
    except Exception as e:
        print(f"Error loading data for {symbol}: {str(e)}")
        return None

def calculate_technical_indicators(df):
    """
    Calculate various technical indicators using ta library
    """
    if len(df) < 50:
        print("Not enough data for technical analysis")
        return df

    try:
        # Moving Averages
        df['SMA_20'] = sma_indicator(close=df['Close'], window=20)
        df['SMA_50'] = sma_indicator(close=df['Close'], window=50)
        df['EMA_20'] = ema_indicator(close=df['Close'], window=20)
        
        # RSI
        rsi_indicator = RSIIndicator(close=df['Close'])
        df['RSI'] = rsi_indicator.rsi()
        
        # MACD
        macd = MACD(close=df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Hist'] = macd.macd_diff()
        
        # Bollinger Bands
        bb = BollingerBands(close=df['Close'])
        df['BB_Upper'] = bb.bollinger_hband()
        df['BB_Middle'] = bb.bollinger_mavg()
        df['BB_Lower'] = bb.bollinger_lband()
        
        # Volume indicators
        df['OBV'] = on_balance_volume(close=df['Close'], volume=df['Volume'])
        
        print("Successfully calculated technical indicators")
        return df
    
    except Exception as e:
        print(f"Error calculating technical indicators: {str(e)}")
        return df

def plot_technical_analysis(df, symbol, output_dir='outputs/technical_analysis'):
    """
    Create visualizations for technical analysis
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Price and Moving Averages
    plt.figure(figsize=(15, 7))
    plt.plot(df.index, df['Close'], label='Close Price', alpha=0.8)
    plt.plot(df.index, df['SMA_20'], label='20-day SMA', alpha=0.7)
    plt.plot(df.index, df['SMA_50'], label='50-day SMA', alpha=0.7)
    plt.title(f'{symbol} Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{symbol}_moving_averages.png')
    plt.close()
    
    # 2. RSI
    plt.figure(figsize=(15, 5))
    plt.plot(df.index, df['RSI'], label='RSI', color='purple')
    plt.axhline(y=70, color='r', linestyle='--', alpha=0.5)
    plt.axhline(y=30, color='g', linestyle='--', alpha=0.5)
    plt.title(f'{symbol} RSI')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{symbol}_rsi.png')
    plt.close()
    
    # 3. MACD
    plt.figure(figsize=(15, 5))
    plt.plot(df.index, df['MACD'], label='MACD', color='blue')
    plt.plot(df.index, df['MACD_Signal'], label='Signal Line', color='orange')
    plt.bar(df.index, df['MACD_Hist'], label='MACD Histogram', alpha=0.3)
    plt.title(f'{symbol} MACD')
    plt.xlabel('Date')
    plt.ylabel('MACD')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{symbol}_macd.png')
    plt.close()
    
    # 4. Bollinger Bands
    plt.figure(figsize=(15, 7))
    plt.plot(df.index, df['Close'], label='Close Price', alpha=0.8)
    plt.plot(df.index, df['BB_Upper'], label='Upper BB', alpha=0.7)
    plt.plot(df.index, df['BB_Middle'], label='Middle BB', alpha=0.7)
    plt.plot(df.index, df['BB_Lower'], label='Lower BB', alpha=0.7)
    plt.fill_between(df.index, df['BB_Upper'], df['BB_Lower'], alpha=0.1)
    plt.title(f'{symbol} Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{symbol}_bollinger_bands.png')
    plt.close()

def main():
    # Define parameters
    symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'NVDA', 'TSLA']  # Example symbols
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 year of data
    
    for symbol in symbols:
        print(f"\nAnalyzing {symbol}...")
        
        # Load data
        df = load_stock_data(symbol, start_date, end_date)
        if df is None:
            continue
            
        # Calculate technical indicators
        df = calculate_technical_indicators(df)
        
        # Create visualizations
        plot_technical_analysis(df, symbol)
        
        # Save processed data
        df.to_csv(f'outputs/technical_analysis/{symbol}_processed_data.csv')
        
        # Print some basic statistics
        print(f"\nSummary Statistics for {symbol}:")
        print("\nLast known indicators:")
        print(f"RSI: {df['RSI'].iloc[-1]:.2f}")
        print(f"MACD: {df['MACD'].iloc[-1]:.2f}")
        print(f"20-day SMA: {df['SMA_20'].iloc[-1]:.2f}")
        print(f"50-day SMA: {df['SMA_50'].iloc[-1]:.2f}")

if __name__ == "__main__":
    main()