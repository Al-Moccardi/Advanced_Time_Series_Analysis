import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_log_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
import numpy as np

st.set_page_config(
    page_title='Nvidia Stock',
    page_icon='📈'
    )

# Titolo
st.title('Nvidia Stock Price')

# Sottotitolo
st.markdown("### Dataset Visualization")

@st.cache_data 
def load_data():
    data = pd.read_csv(r'C:\Users\ALBER\OneDrive\Desktop\streamlit\NVDA.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    return data


data = load_data()

# Imposta la data più recente come valore predefinito per il widget date_input
default_end_date = data['Date'].max()

# Sidebar per selezionare un range di date
st.sidebar.subheader("Seleziona un range di date")
start_date = st.sidebar.date_input("Data di inizio", min_value=data['Date'].min(), max_value=default_end_date, value=data['Date'].min())
end_date = st.sidebar.date_input("Data di fine", min_value=start_date, max_value=default_end_date, value=default_end_date)

# Converti start_date e end_date in datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filtraggio dei dati in base al range di date selezionato
filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

# Mostra i dati del DataFrame
if st.checkbox("Mostra i dati", False):
    st.write(filtered_data)

# Sidebar per selezionare quali colonne visualizzare nel grafico a linea
st.sidebar.subheader("Seleziona le colonne da visualizzare nel grafico a linea")
show_open = st.sidebar.checkbox("Open", value=True)
show_close = st.sidebar.checkbox("Close", value=True)
show_low = st.sidebar.checkbox("Low", value=True)
show_high = st.sidebar.checkbox("High", value=True)
# Sidebar per selezionare se visualizzare il volume su un asse y secondario
show_volume = st.sidebar.checkbox("Volume", value=False)

# Grafico a linea
st.markdown("### Grafico a linea")
fig_line = go.Figure()

# Aggiungi traccia per Open se selezionato
if show_open:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Open'], mode='lines', name='Open'))

# Aggiungi traccia per Close se selezionato
if show_close:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Close'], mode='lines', name='Close'))

# Aggiungi traccia per Low se selezionato
if show_low:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Low'], mode='lines', name='Low'))

# Aggiungi traccia per High se selezionato
if show_high:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['High'], mode='lines', name='High'))

# Aggiungi traccia per il volume come linea su un'asse y2 se selezionato
if show_volume:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Volume'], mode='lines', name='Volume', yaxis='y2'))

# Aggiorna il layout del grafico per includere un asse y2 se il volume è selezionato
if show_volume:
    fig_line.update_layout(yaxis2=dict(title='Volume', overlaying='y', side='right'))

st.plotly_chart(fig_line)

# Grafico a candela
st.markdown("### Grafico a candela")
fig_candle = go.Figure(data=[go.Candlestick(x=filtered_data['Date'],
                                             open=filtered_data['Open'],
                                             high=filtered_data['High'],
                                             low=filtered_data['Low'],
                                             close=filtered_data['Close'])])
st.plotly_chart(fig_candle)

# Grafico OHLC
st.markdown("### Grafico OHLC")
fig_ohlc = go.Figure(data=[go.Ohlc(x=filtered_data['Date'],
                                   open=filtered_data['Open'],
                                   high=filtered_data['High'],
                                   low=filtered_data['Low'],
                                   close=filtered_data['Close'])])
st.plotly_chart(fig_ohlc)

# Selezione del valore per la media mobile
st.sidebar.subheader("Seleziona un valore per la media mobile")
window = st.sidebar.slider("Valore per la media mobile", min_value=2, max_value=50, value=10)

# Calcolo della media mobile e visualizzazione sul grafico a linea
st.markdown("### Media mobile di Close")
filtered_data['Close_Moving_Avg'] = filtered_data['Close'].rolling(window=window).mean()
fig_avg = go.Figure()
fig_avg.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Close'], mode='lines', name='Close'))
fig_avg.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Close_Moving_Avg'], mode='lines', name='Moving Average'))
fig_avg.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(fig_avg)


#----------------------------- Prophet Forecasting------------------------------------------#

# Prophet sidebar
st.sidebar.subheader('Prophet parameters configuration')
horizon_selection = st.sidebar.slider('Forecasting horizon (days)', min_value=1, max_value=365, value=90)
growth_selection = st.sidebar.radio(label='Growth', options=['linear', 'logistic'])
if growth_selection == 'logistic':
    st.sidebar.info('Configure logistic growth saturation as a percentage of latest Close')
    cap = st.sidebar.slider('Constant carrying capacity', min_value=1.0, max_value=1.5, value=1.2)
    cap_close = cap*data['Close'].iloc[-1]
    data['cap']=cap_close
seasonality_selection = st.sidebar.radio(label='Seasonality', options=['additive', 'multiplicative'])
with st.sidebar.expander('Seasonality components'):
    weekly_selection = st.checkbox('Weekly')
    monthly_selection = st.checkbox('Monthly', value=True)
    yearly_selection = st.checkbox('Yearly', value=True)
with open(r'C:\Users\ALBER\OneDrive\Desktop\streamlit\holiday_countries.txt', 'r') as fp:
    holiday_country_list = fp.read().split('\n')
    holiday_country_list.insert(0, 'None')
holiday_country_selection = st.sidebar.selectbox(label="Holiday country", options=holiday_country_list)


st.header('Prophet Forecasting')
# Prophet model fitting
with st.spinner('Model fitting..'):
    prophet_df = data.rename(columns={'Date': 'ds', 'Close': 'y'})
    model = Prophet(
        seasonality_mode=seasonality_selection,
        weekly_seasonality=weekly_selection,
        yearly_seasonality=yearly_selection,
        growth=growth_selection,
        )
    if holiday_country_selection != 'None':
        model.add_country_holidays(country_name=holiday_country_selection)      
    if monthly_selection:
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    model.fit(prophet_df)

# Prophet model forecasting
with st.spinner('Making predictions..'):
    future = model.make_future_dataframe(periods=horizon_selection, freq='D')
    if growth_selection == 'logistic':
        future['cap'] = cap_close
    forecast = model.predict(future)

# Prophet forecast plot
fig = px.scatter(prophet_df, x='ds', y='y', labels={'ds': 'Day', 'y': 'Close'})
fig.add_scatter(x=forecast['ds'], y=forecast['yhat'], name='yhat')
fig.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='yhat_lower')
fig.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='yhat_upper')
st.plotly_chart(fig)