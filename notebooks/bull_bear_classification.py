#!/usr/bin/env python
# coding: utf-8

# In[17]:


import yfinance as yf
import pandas as pd

# Download S&P 500 data from 2000 to present
sp500 = yf.download("SPY", start="1900-01-01", end="2024-12-31", interval="1d")
# Flatten the MultiIndex into single-level column names
sp500.columns = ['_'.join(col).strip() for col in sp500.columns.values]
sp500.reset_index(inplace=True)
print(sp500.head())



# Save data to a CSV file
sp500.to_csv("../data/raw/sp500.csv", index=True)

# Check the first few rows
print(sp500.head())
print(sp500.columns)

from fredapi import Fred

# Set up FRED API
fred = Fred(api_key='e916710d165717e6348556cdce8111f3')

# Fetch economic indicators
gdp = fred.get_series('GDP')  # Quarterly GDP data
cpi = fred.get_series('CPIAUCSL')  # Consumer Price Index
unemployment = fred.get_series('UNRATE')  # Unemployment rate

# Save data to CSV files
gdp.to_csv("../data/raw/gdp.csv")
cpi.to_csv("../data/raw/cpi.csv")
unemployment.to_csv("../data/raw/unemployment.csv")

# Check GDP data
print(gdp.head())

# Load S&P 500 data
sp500 = pd.read_csv("../data/raw/sp500.csv", index_col="Date", parse_dates=True)

# Calculate daily percentage change
sp500['pct_change'] = sp500['Close_SPY'].pct_change()

# Define rolling window for trends (e.g., 20-day rolling average)
sp500['trend'] = sp500['Close_SPY'].rolling(window=20).mean()

# Label bull/bear markets based on thresholds
sp500['market_label'] = sp500['pct_change'].apply(lambda x: 'Bull' if x > 0.05 else 'Bear')

# Save labeled data
sp500.to_csv("../data/processed/sp500_labeled.csv")


# In[ ]:




