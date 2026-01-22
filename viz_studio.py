# filename: viz_studio.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class VizStudio:
    """
    The rendering engine for Jeavily.
    Produces Plotly figure objects for the Hex frontend.
    """
    
    @staticmethod
    def plot_entanglement_heatmap(corr_matrix):
        """
        Renders the correlation matrix as a sleek dark-mode heatmap.
        """
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu_r', # Red (negative) to Blue (positive)
            title="The Entanglement Map: Hidden Correlations"
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)', # Transparent background
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Courier New, monospace") # The 'Coder' font
        )
        return fig

    @staticmethod
    def plot_shock_timeline(ticker, df, shocks):
        """
        Overlays 'Shock' points on the main price line.
        """
        fig = go.Figure()
        
        # Main Price Line
        fig.add_trace(go.Scatter(
            x=df['timestamp'], 
            y=df['probability'],
            mode='lines',
            name=f'{ticker} Price',
            line=dict(color='#00F0FF', width=2) # Cyberpunk Cyan
        ))
        
        # Shock Markers
        shock_dates = df.loc[shocks, 'timestamp']
        shock_prices = df.loc[shocks, 'probability']
        
        fig.add_trace(go.Scatter(
            x=shock_dates,
            y=shock_prices,
            mode='markers',
            name='Volatility Shock (>3σ)',
            marker=dict(color='#FF0055', size=10, symbol='x') # Cyberpunk Red
        ))
        
        fig.update_layout(
            template="plotly_dark",
            title=f"Market Stress Test: {ticker}",
            yaxis_title="Implied Probability",
            font=dict(family="Courier New, monospace")
        )
        return fig
