# filename: entropy_engine.py
import pandas as pd
import numpy as np
from scipy.stats import zscore

class EntropyEngine:
    """
    The mathematical core of Jeavily. 
    Calculates volatility shocks and market entanglement.
    """

    @staticmethod
    def calculate_rolling_volatility(series, window=24):
        """
        Calculates rolling volatility (std dev) and normalizes it.
        Assumes hourly data (window=24).
        """
        # Log returns are more stable for volatility calculation
        log_rets = np.log(series / series.shift(1))
        vol = log_rets.rolling(window=window).std()
        return vol

    @staticmethod
    def detect_shocks(df, threshold=3.0):
        """
        Identifies 'Shock' moments where volatility exceeds Z-Score threshold.
        Returns a boolean mask of shock events.
        """
        # Calculate Z-score of the price changes
        # fillna(0) to handle the first few rows of NaN
        changes = df.pct_change().fillna(0)
        z_scores = np.abs(zscore(changes))
        
        # Return moments where the market 'panicked' (Z > threshold)
        return z_scores > threshold

    @staticmethod
    def compute_entanglement_matrix(df_dict):
        """
        Input: Dictionary of DataFrames {ticker: df}
        Output: Correlation Matrix
        
        This aligns disparate timeframes (e.g., a market that started yesterday 
        vs one that started last month) to finding common movements.
        """
        # 1. Extract the 'Yes' price probability from each market
        combined_prices = pd.DataFrame()
        
        for ticker, data in df_dict.items():
            if 'probability' in data.columns:
                # Resample to hourly to align timestamps
                # We use 'ffill' because prediction markets aren't always liquid every minute
                combined_prices[ticker] = data.set_index('timestamp')['probability'].resample('1H').ffill()
        
        # 2. Compute Pearson Correlation
        # We drop NaNs to only correlate overlapping periods
        correlation_matrix = combined_prices.corr(method='pearson')
        
        # Filter: Zero out weak correlations to reduce noise in the viz
        # This makes the "High Signal" connections pop
        correlation_matrix[np.abs(correlation_matrix) < 0.3] = 0
        
        return correlation_matrix

    @staticmethod
    def get_butterfly_index(correlation_matrix):
        """
        Returns the pair of markets with the highest unexpected correlation.
        """
        # Mask diagonal (self-correlation is always 1.0)
        np.fill_diagonal(correlation_matrix.values, 0)
        
        # Find max value
        max_corr = correlation_matrix.max().max()
        # Get the pair
        # (This is a simplified finder for the MVP)
        return max_corr
