from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset we're interested in
        self.ticker = "AAPL"
        
    @property
    def interval(self):
        # We'll analyze data on a daily basis
        return "1day"
    
    @property
    def assets(self):
        # List of assets this strategy will handle
        return [self.ticker]
    
    def run(self, data):
        # Get close price data for the SMA calculations
        ohlcv = data["ohlcv"]
        
        # Calculate the short-term and long-term SMAs
        short_sma = SMA(self.ticker, ohlcv, length=20)
        long_sma = SMA(self.ticker, ohlcv, length=50)
        
        # Initialize allocation as none
        allocation = 0
        
        # Check if enough data points are available
        if len(short_sma) > 50 and len(long_sma) > 50:
            # Check for the crossover condition to go long
            if short_sma[-1] > long_sma[-1] and short_sma[-2] <= long_sma[-2]:
                log("Going long")
                allocation = 1  # 100% allocation
            # Check for the crossover condition to exit or go short (optional)
            elif short_sma[-1] < long_sma[-1] and short_sma[-2] >= long_sma[-2]:
                log("Exiting position")
                allocation = 0  # 0% allocation, exit the position
            
        # Return the calculated allocation
        return TargetAllocation({self.ticker: allocation})