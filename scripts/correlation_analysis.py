import pandas as pd
import numpy as np
from textblob import TextBlob
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def load_and_prepare_data(stock_file, run_analysis_file):
    """
    Load and prepare both stock and news data from run_analysis output
    """
    try:
        # Load processed stock data (already has technical indicators)
        stock_df = pd.read_csv(stock_file)
        stock_df['Date'] = pd.to_datetime(stock_df['Date'])
        stock_df.set_index('Date', inplace=True)
        
        # Calculate daily returns if not already present
        if 'Returns' not in stock_df.columns:
            stock_df['Returns'] = stock_df['Close'].pct_change()
        
        # Load news sentiment data from run_analysis
        news_df = pd.read_csv(run_analysis_file)
        
        # Ensure date column is datetime
        if 'date' in news_df.columns:
            news_df['Date'] = pd.to_datetime(news_df['date'])
        else:
            news_df['Date'] = pd.to_datetime(news_df['Date'])
        
        # Calculate daily sentiment scores
        daily_sentiment = news_df.groupby('Date').agg({
            'sentiment': ['mean', 'count']
        }).reset_index()
        
        daily_sentiment.columns = ['Date', 'avg_sentiment', 'news_count']
        
        print("Data loaded successfully")
        return stock_df, daily_sentiment
    
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        # Print more detailed error information
        import traceback
        print(traceback.format_exc())
        return None, None

def analyze_technical_correlations(df):
    """
    Analyze correlations between different technical indicators and price movements
    """
    # Calculate daily returns if not already present
    if 'Returns' not in df.columns:
        df['Returns'] = df['Close'].pct_change()
    
    # Define the indicators to analyze
    indicators = ['RSI', 'MACD', 'MACD_Signal', 'MACD_Hist', 'OBV']
    
    # Create correlation matrix
    correlation_data = df[['Returns'] + indicators].dropna()
    correlation_matrix = correlation_data.corr()
    
    # Calculate lagged correlations for each indicator
    lagged_correlations = {}
    for indicator in indicators:
        lags = []
        for i in range(1, 4):  # Check correlations for t+1, t+2, t+3
            lag_corr = df['Returns'].corr(df[indicator].shift(i))
            lags.append((i, lag_corr))
        lagged_correlations[indicator] = lags
    
    return correlation_matrix, lagged_correlations

def plot_technical_correlations(df, output_dir):
    """
    Create visualization for technical indicator correlations
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Correlation heatmap
    plt.figure(figsize=(10, 8))
    indicators = ['Returns', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Hist', 'OBV']
    correlation_matrix = df[indicators].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Technical Indicators Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlation_heatmap.png')
    plt.close()
    
    # 2. RSI vs Returns scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df['RSI'], df['Returns'], alpha=0.5)
    plt.title('RSI vs Daily Returns')
    plt.xlabel('RSI')
    plt.ylabel('Daily Returns')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/rsi_returns_scatter.png')
    plt.close()
    
    # 3. MACD histogram vs Returns
    plt.figure(figsize=(10, 6))
    plt.scatter(df['MACD_Hist'], df['Returns'], alpha=0.5)
    plt.title('MACD Histogram vs Daily Returns')
    plt.xlabel('MACD Histogram')
    plt.ylabel('Daily Returns')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/macd_hist_returns_scatter.png')
    plt.close()

def main():
    # Define parameters
    symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'NVDA', 'TSLA']
    
    for symbol in symbols:
        print(f"\nAnalyzing {symbol}...")
        
        # Load technical analysis data
        file_path = f'outputs/technical_analysis/{symbol}_processed_data.csv'
        try:
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
            # Calculate correlations
            correlation_matrix, lagged_correlations = analyze_technical_correlations(df)
            
            # Create visualizations
            plot_technical_correlations(df, f'outputs/correlation_analysis/{symbol}')
            
            # Print results
            print(f"\nCorrelation Analysis Results for {symbol}:")
            print("\nSame-day correlations:")
            print(correlation_matrix['Returns'].round(4))
            
            print("\nLagged correlations:")
            for indicator, lags in lagged_correlations.items():
                print(f"\n{indicator}:")
                for lag, corr in lags:
                    print(f"t+{lag} correlation: {corr:.4f}")
            
        except Exception as e:
            print(f"Error analyzing {symbol}: {str(e)}")
            continue

if __name__ == "__main__":
    main()