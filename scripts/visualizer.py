import matplotlib.pyplot as plt
import seaborn as sns

def plot_sentiment_vs_price(df, sentiment_col='sentiment', price_col='Close'):
    """Plot sentiment scores against stock prices."""
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sentiment', color='tab:blue')
    ax1.plot(df.index, df[sentiment_col], color='tab:blue', label='Sentiment')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Stock Price', color='tab:orange')
    ax2.plot(df.index, df[price_col], color='tab:orange', label='Stock Price')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    plt.title('News Sentiment vs Stock Price')
    fig.tight_layout()
    plt.show()

def plot_correlation_heatmap(df, columns):
    """Plot a correlation heatmap for specified columns."""
    corr = df[columns].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title('Correlation Heatmap')
    plt.show()

