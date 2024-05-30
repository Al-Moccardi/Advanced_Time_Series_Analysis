import pandas as pd

def preprocess_data(data, start_date, end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    return data
