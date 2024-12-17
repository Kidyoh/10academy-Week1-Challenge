import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_news_data
from sentiment_analyzer import apply_sentiment_analysis
from datetime import datetime

def perform_descriptive_statistics(df):
    print("\n=== Descriptive Statistics ===")
    
    # Headline length analysis
    df['headline_length'] = df['headline'].str.len()
    print("\nHeadline Length Statistics:")
    print(df['headline_length'].describe())
    
    # Publisher analysis
    print("\nTop 10 Publishers by Article Count:")
    publisher_counts = df['publisher'].value_counts().head(10)
    print(publisher_counts)
    
    # Create visualizations
    plt.figure(figsize=(12, 6))
    publisher_counts.plot(kind='bar')
    plt.title('Top 10 Publishers by Article Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/publisher_distribution.png')
    plt.close()

def perform_time_analysis(df):
    print("\n=== Time Series Analysis ===")
    
    # Ensure date column is datetime
    try:
        df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
        print(f"Number of valid dates: {df['date'].notna().sum()}")
        print(f"Number of invalid dates: {df['date'].isna().sum()}")
        
        # Remove rows with invalid dates
        df = df.dropna(subset=['date'])
        
        # Add time-based features
        df['hour'] = df['date'].dt.hour
        df['day_of_week'] = df['date'].dt.day_name()
        df['month'] = df['date'].dt.month
        
        # Articles per day
        daily_counts = df.groupby(df['date'].dt.date).size()
        print("\nDaily Article Statistics:")
        print(daily_counts.describe())
# Visualize publication patterns
        plt.figure(figsize=(12, 6))
        daily_counts.plot()
        plt.title('Number of Articles Published Over Time')
        plt.tight_layout()
        plt.savefig('outputs/daily_publication_trend.png')
        plt.close()
        
        # Hour of day analysis
        plt.figure(figsize=(10, 6))
        df['hour'].value_counts().sort_index().plot(kind='bar')
        plt.title('Distribution of Publication Hours')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Articles')
        plt.tight_layout()
        plt.savefig('outputs/hourly_distribution.png')
        plt.close()

    except Exception as e:
            print(f"Error in time analysis: {str(e)}")
            print("\nDebug information:")
            print(f"Date column type: {df['date'].dtype}")
            print("\nFirst few dates:")
            print(df['date'].head())



def analyze_sentiment_distribution(df):
    print("\n=== Sentiment Analysis ===")
    
    # Apply sentiment analysis
    df = apply_sentiment_analysis(df)
    
    # Print sentiment distribution
    print("\nSentiment Distribution:")
    print(df['sentiment'].value_counts(normalize=True))
    
    # Visualize sentiment distribution
    plt.figure(figsize=(8, 6))
    df['sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Sentiment in Headlines')
    plt.tight_layout()
    plt.savefig('outputs/sentiment_distribution.png')
    plt.close()
    
    return df

def main():
    # Load the financial news dataset
    print("Loading news data...")
    news_df = load_news_data('data/rawanalyst_data/raw_analyst_ratings.csv')
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('outputs', exist_ok=True)
    
    # Perform analyses
    perform_descriptive_statistics(news_df)
    perform_time_analysis(news_df)
    news_df = analyze_sentiment_distribution(news_df)
    
    # Save processed dataset
    news_df.to_csv('outputs/processed_news_data.csv', index=False)
    print("\nAnalysis complete. Check the 'outputs' directory for visualizations.")

if __name__ == "__main__":
    main()