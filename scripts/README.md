# Stock Market Analysis Project

A comprehensive Python-based stock market analysis tool that combines technical analysis with advanced visualization capabilities.

## Overview

This project provides a robust framework for analyzing stock market data through technical indicators and correlation analysis. It processes historical stock data to generate actionable insights through various technical analysis methods.

## Features

### Technical Analysis (`scripts/technical_analysis.py`)
- **Price Indicators**
  - Simple Moving Averages (SMA 20 and 50 days)
  - Exponential Moving Average (EMA 20 days)
  - Bollinger Bands (20-day, 2 standard deviations)

- **Momentum Indicators**
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
    - MACD Line (12/26 periods)
    - Signal Line (9-day EMA of MACD)
    - MACD Histogram

- **Volume Indicators**
  - On Balance Volume (OBV)

### Correlation Analysis (`scripts/correlation_analysis.py`)
- Cross-indicator correlation analysis
- Lagged correlation studies (t+1, t+2, t+3)
- Technical indicator effectiveness evaluation
- Visual correlation analysis through heatmaps and scatter plots

### Visualizations
- Interactive price charts with technical overlays
- RSI momentum visualization
- MACD signal analysis charts
- Bollinger Bands trend analysis
- Correlation heatmaps
- Technical indicator scatter plots


## Usage

1. Prepare your data:
   - Place historical stock data CSV files in `data/yfinance_data/`
   - Files should be named as `{SYMBOL}_historical_data.csv`
   - Required columns: Date, Open, High, Low, Close, Volume

2. Run the analysis:
   - Run `python scripts/technical_analysis.py` to generate technical analysis data
   - Run `python scripts/correlation_analysis.py` to generate correlation analysis data


3. View results:
   - Technical analysis outputs in `outputs/technical_analysis/`
   - Correlation analysis results in `outputs/correlation_analysis/`

## Output Structure

### Technical Analysis Results (`outputs/technical_analysis/`)
- Processed CSV files containing:
  - Original price and volume data
  - Moving averages (SMA 20, SMA 50, EMA 20)
  - RSI values
  - MACD components
  - Bollinger Bands
  - OBV values
- Visualization charts:
  - Price with moving averages and Bollinger Bands
  - RSI indicator chart
  - MACD signal chart
  - Volume and OBV analysis

### Correlation Analysis Results (`outputs/correlation_analysis/`)
- Correlation matrices showing relationships between:
  - Price movements and technical indicators
  - Different technical indicators
  - Lagged correlations for predictive analysis
- Visualization plots:
  - Correlation heatmaps
  - RSI vs Returns scatter plots
  - MACD histogram vs Returns scatter plots
  - Time-lagged correlation charts

## Technical Details

### Data Processing
- Handles missing data through forward filling
- Calculates daily returns for correlation analysis
- Implements proper date indexing
- Manages data alignment for technical indicators

### Technical Indicators
- **SMA**: 20 and 50-day periods for trend identification
- **EMA**: 20-day period with proper decay factor
- **RSI**: 14-day period with oversold/overbought levels
- **MACD**: 12/26 day EMAs with 9-day signal line
- **Bollinger Bands**: 20-day SMA with 2 standard deviations
- **OBV**: Cumulative volume indicator with price direction

### Statistical Analysis
- Pearson correlation coefficients
- Lagged correlation analysis (t+1 to t+3)
- Statistical significance testing
- Outlier detection and handling

## Dependencies
- Python 3.8+
- pandas >= 1.2.0
- numpy >= 1.19.0
- matplotlib >= 3.3.0
- seaborn >= 0.11.0
- yfinance >= 0.1.63

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Include docstrings for new functions
- Add unit tests for new features
- Update documentation as needed


