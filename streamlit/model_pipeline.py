import pandas as pd
from prophet import Prophet
import plotly.express as px

def prophet_forecast(data, horizon, growth, seasonality_mode, weekly_seasonality, monthly_seasonality, yearly_seasonality, holidays):
    data = data.rename(columns={'Date': 'ds', 'Close': 'y'})
    
    model = Prophet(
        growth=growth,
        seasonality_mode=seasonality_mode,
        weekly_seasonality=weekly_seasonality,
        yearly_seasonality=yearly_seasonality
    )

    if holidays != 'None':
        model.add_country_holidays(country_name=holidays)
        
    if monthly_seasonality:
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    
    model.fit(data)
    future = model.make_future_dataframe(periods=horizon)
    
    if growth == 'logistic':
        cap = 1.2 * data['y'].max()
        data['cap'] = cap
        future['cap'] = cap
        
    forecast = model.predict(future)
    
    fig = px.scatter(data, x='ds', y='y', labels={'ds': 'Date', 'y': 'Close'})
    fig.add_scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast')
    fig.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dash'))
    fig.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dash'))
    
    return forecast, fig
