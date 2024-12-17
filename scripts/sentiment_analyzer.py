from textblob import TextBlob

def analyze_sentiment(text):
    """Perform sentiment analysis on a given text."""
    return TextBlob(text).sentiment.polarity

def apply_sentiment_analysis(df, text_column='headline'):
    """Apply sentiment analysis to a DataFrame column."""
    df['sentiment'] = df[text_column].apply(analyze_sentiment)
    return df

