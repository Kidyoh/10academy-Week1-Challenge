import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import yfinance as yf
from datetime import datetime, timedelta

def create_report_directory():
    """Create directory for report plots"""
    Path('reports/plots').mkdir(parents=True, exist_ok=True)
    return 'reports/plots'

def plot_1_price_technical(symbol='TSLA'):
    """Plot 1: Price with Technical Overlays"""
    df = pd.read_csv(f'outputs/technical_analysis/{symbol}_processed_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='Price', color='blue')
    plt.plot(df['Date'], df['SMA_20'], label='20-day SMA', color='orange')
    plt.plot(df['Date'], df['BB_Upper'], label='Upper BB', color='red', linestyle='--')
    plt.plot(df['Date'], df['BB_Lower'], label='Lower BB', color='red', linestyle='--')
    
    plt.title(f'{symbol} Price with Technical Overlays')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot1_technical_overlay.png')
    plt.close()

def plot_2_rsi_comparison(symbols=['NVDA', 'META', 'TSLA']):
    """Plot 2: RSI Comparison"""
    plt.figure(figsize=(12, 6))
    
    for symbol in symbols:
        df = pd.read_csv(f'outputs/technical_analysis/{symbol}_processed_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        plt.plot(df['Date'], df['RSI'], label=symbol)
    
    plt.axhline(y=70, color='r', linestyle='--')
    plt.axhline(y=30, color='r', linestyle='--')
    plt.title('RSI Comparison Across Stocks')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot2_rsi_comparison.png')
    plt.close()

def plot_3_obv_trends(symbols=['NVDA', 'TSLA', 'AAPL']):
    """Plot 3: OBV Trends"""
    plt.figure(figsize=(12, 6))
    
    for symbol in symbols:
        df = pd.read_csv(f'outputs/technical_analysis/{symbol}_processed_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        # Normalize OBV for comparison
        df['OBV_norm'] = (df['OBV'] - df['OBV'].min()) / (df['OBV'].max() - df['OBV'].min())
        plt.plot(df['Date'], df['OBV_norm'], label=symbol)
    
    plt.title('Normalized OBV Trends')
    plt.xlabel('Date')
    plt.ylabel('Normalized OBV')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot3_obv_trends.png')
    plt.close()

def plot_4_correlation_heatmap(symbol='TSLA'):
    """Plot 4: Technical Indicator Correlation Heatmap"""
    df = pd.read_csv(f'outputs/technical_analysis/{symbol}_processed_data.csv')
    
    # Calculate returns
    df['Returns'] = df['Close'].pct_change()
    
    # Select indicators for correlation
    indicators = ['Returns', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Hist', 'OBV']
    corr_matrix = df[indicators].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title(f'{symbol} Technical Indicator Correlations')
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot4_correlation_heatmap.png')
    plt.close()

def plot_5_lagged_correlations(symbol='TSLA'):
    """Plot 5: Lagged Correlation Results"""
    df = pd.read_csv(f'outputs/technical_analysis/{symbol}_processed_data.csv')
    df['Returns'] = df['Close'].pct_change()
    
    indicators = ['RSI', 'MACD', 'OBV']
    lags = range(1, 4)
    
    lag_corrs = {}
    for indicator in indicators:
        lag_corrs[indicator] = [df['Returns'].corr(df[indicator].shift(lag)) for lag in lags]
    
    plt.figure(figsize=(10, 6))
    for indicator in indicators:
        plt.plot(lags, lag_corrs[indicator], marker='o', label=indicator)
    
    plt.title('Lagged Correlations with Returns')
    plt.xlabel('Lag (days)')
    plt.ylabel('Correlation')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot5_lagged_correlations.png')
    plt.close()

def plot_6_nvda_dashboard():
    """Plot 6: NVDA Technical Analysis Dashboard"""
    df = pd.read_csv('outputs/technical_analysis/NVDA_processed_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    fig, axs = plt.subplots(3, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1, 1]})
    
    # Price and MAs
    axs[0].plot(df['Date'], df['Close'], label='Price')
    axs[0].plot(df['Date'], df['SMA_20'], label='SMA20')
    axs[0].plot(df['Date'], df['SMA_50'], label='SMA50')
    axs[0].set_title('NVDA Price and Moving Averages')
    axs[0].legend()
    
    # RSI
    axs[1].plot(df['Date'], df['RSI'])
    axs[1].axhline(y=70, color='r', linestyle='--')
    axs[1].axhline(y=30, color='r', linestyle='--')
    axs[1].set_title('RSI')
    
    # MACD
    axs[2].plot(df['Date'], df['MACD'], label='MACD')
    axs[2].plot(df['Date'], df['MACD_Signal'], label='Signal')
    axs[2].bar(df['Date'], df['MACD_Hist'], label='Histogram', alpha=0.3)
    axs[2].set_title('MACD')
    axs[2].legend()
    
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot6_nvda_dashboard.png')
    plt.close()

def plot_7_tesla_volatility():
    """Plot 7: TSLA Volatility Analysis"""
    df = pd.read_csv('outputs/technical_analysis/TSLA_processed_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Returns'] = df['Close'].pct_change()
    df['Volatility'] = df['Returns'].rolling(20).std() * np.sqrt(252)  # Annualized
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    ax1.plot(df['Date'], df['Close'], color='blue', label='Price')
    ax1.set_ylabel('Price', color='blue')
    
    ax2 = ax1.twinx()
    ax2.plot(df['Date'], df['Volatility'], color='red', label='Volatility')
    ax2.set_ylabel('Volatility', color='red')
    
    plt.title('TSLA Price and Volatility')
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot7_tesla_volatility.png')
    plt.close()

def plot_8_apple_patterns():
    """Plot 8: AAPL Technical Patterns"""
    df = pd.read_csv('outputs/technical_analysis/AAPL_processed_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='Price')
    plt.plot(df['Date'], df['BB_Upper'], label='Upper BB', linestyle='--')
    plt.plot(df['Date'], df['BB_Middle'], label='Middle BB')
    plt.plot(df['Date'], df['BB_Lower'], label='Lower BB', linestyle='--')
    
    plt.title('AAPL Bollinger Band Pattern Analysis')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot8_apple_patterns.png')
    plt.close()

def plot_9_risk_metrics(symbols=['AAPL', 'NVDA', 'TSLA', 'META', 'GOOG']):
    """Plot 9: Risk Metrics Comparison"""
    risk_metrics = []
    
    for symbol in symbols:
        df = pd.read_csv(f'outputs/technical_analysis/{symbol}_processed_data.csv')
        df['Returns'] = df['Close'].pct_change()
        
        volatility = df['Returns'].std() * np.sqrt(252)
        max_drawdown = (df['Close'] / df['Close'].cummax() - 1).min()
        
        risk_metrics.append({
            'Symbol': symbol,
            'Volatility': volatility,
            'Max Drawdown': max_drawdown
        })
    
    risk_df = pd.DataFrame(risk_metrics)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(symbols))
    width = 0.35
    
    ax.bar(x - width/2, risk_df['Volatility'], width, label='Volatility')
    ax.bar(x + width/2, risk_df['Max Drawdown'], width, label='Max Drawdown')
    
    ax.set_xticks(x)
    ax.set_xticklabels(symbols)
    ax.set_title('Risk Metrics Comparison')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot9_risk_metrics.png')
    plt.close()

def plot_10_predictive_performance(symbol='TSLA'):
    """Plot 10: Predictive Model Performance"""
    df = pd.read_csv(f'outputs/technical_analysis/{symbol}_processed_data.csv')
    df['Returns'] = df['Close'].pct_change()
    
    # Simple prediction using RSI
    df['Prediction'] = np.where(df['RSI'] < 30, 1, np.where(df['RSI'] > 70, -1, 0))
    df['Next_Return'] = df['Returns'].shift(-1)
    
    plt.figure(figsize=(12, 6))
    plt.scatter(df['RSI'], df['Next_Return'], alpha=0.5)
    plt.axvline(x=30, color='r', linestyle='--')
    plt.axvline(x=70, color='r', linestyle='--')
    
    plt.title(f'{symbol} RSI vs Next-Day Returns')
    plt.xlabel('RSI')
    plt.ylabel('Next-Day Return')
    plt.tight_layout()
    plt.savefig(f'{report_dir}/plot10_predictive_performance.png')
    plt.close()

def main():
    global report_dir
    report_dir = create_report_directory()
    
    # Generate all plots
    plot_1_price_technical()
    plot_2_rsi_comparison()
    plot_3_obv_trends()
    plot_4_correlation_heatmap()
    plot_5_lagged_correlations()
    plot_6_nvda_dashboard()
    plot_7_tesla_volatility()
    plot_8_apple_patterns()
    plot_9_risk_metrics()
    plot_10_predictive_performance()

if __name__ == "__main__":
    main()