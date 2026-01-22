# filename: kalshi_loader.py
import requests
import pandas as pd
from datetime import datetime, timedelta

class JeavilyLoader:
    """
    The ingestion layer for Jeavily. 
    Handles API negotiation and data normalization.
    """
    
    def __init__(self):
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2" # Public endpoint for election cycle, or use general v2
        self.headers = {"Accept": "application/json"}

    def fetch_markets(self, limit=100):
        """
        Fetches active markets. 
        Refines raw JSON into a high-performance Pandas DataFrame.
        """
        # In a real heavy-lift scenario, we'd paginate. 
        # For the hackathon, we grab the snapshot.
        try:
            # Using the public markets endpoint
            url = f"{self.base_url}/markets" 
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            # fast-fail if API changes
            if 'markets' not in data:
                return pd.DataFrame() 

            df = pd.DataFrame(data['markets'])
            
            # The "Genius" Filter:
            # We only care about high-signal markets (Active & Liquid)
            mask = (df['status'] == 'active')
            clean_df = df[mask].copy()
            
            # Normalize timestamp for time-series analysis
            clean_df['open_date'] = pd.to_datetime(clean_df['open_date'])
            
            print(f"⚡ Jeavily Ingest: {len(clean_df)} active markets loaded.")
            return clean_df
            
        except Exception as e:
            print(f"CRITICAL: Data ingestion failed - {e}")
            return pd.DataFrame()

    def get_market_history(self, ticker):
        """
        Drills down into a specific ticker for time-series data.
        """
        # Placeholder logic for specific ticker history
        # In a rush, we might simulate this or use a secondary dataset
        pass

# Quick test execution
if __name__ == "__main__":
    loader = JeavilyLoader()
    markets = loader.fetch_markets()
    print(markets.head())
