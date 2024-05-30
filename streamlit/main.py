import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from preprocessing import preprocess_data
from model_pipeline import prophet_forecast

# Set Streamlit page configuration
st.set_page_config(
    page_title='Nvidia Stock Analysis',
    page_icon='📈',
    layout='wide'
)

# Custom CSS for styling
st.markdown("""
    <style>
        .main-header {
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
        }
        .reportview-container .main .block-container {
            padding: 20px;
            border-radius: 10px;
            background-color: #ffffff;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #4CAF50;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            text-align: center;
            font-size: 14px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stCheckbox>div>div {
            font-size: 14px;
            margin-bottom: 10px;
        }
        .stSlider>div>div>div {
            color: #000;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='main-header'>Nvidia Stock Price Analysis</h1>", unsafe_allow_html=True)
st.markdown("""
This application provides an analysis of Nvidia's stock prices using various visualizations and a forecasting model.
""")

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('NVDA.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    return data

data = load_data()

# Sidebar for date range selection
st.sidebar.subheader("Select Date Range")
start_date = st.sidebar.date_input("Start Date", min_value=data['Date'].min(), max_value=data['Date'].max(), value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", min_value=start_date, max_value=data['Date'].max(), value=data['Date'].max())

# Filter data based on selected date range
filtered_data = preprocess_data(data, start_date, end_date)

# Display filtered data
if st.checkbox("Show Data", False):
    st.write(filtered_data)

# Sidebar for line chart options
st.sidebar.subheader("Line Chart Options")
show_open = st.sidebar.checkbox("Open", value=True)
show_close = st.sidebar.checkbox("Close", value=True)
show_low = st.sidebar.checkbox("Low", value=True)
show_high = st.sidebar.checkbox("High", value=True)
show_volume = st.sidebar.checkbox("Volume", value=False)

# Line Chart
st.markdown("### Line Chart")
fig_line = go.Figure()

if show_open:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Open'], mode='lines', name='Open'))
if show_close:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Close'], mode='lines', name='Close'))
if show_low:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Low'], mode='lines', name='Low'))
if show_high:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['High'], mode='lines', name='High'))
if show_volume:
    fig_line.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Volume'], mode='lines', name='Volume', yaxis='y2'))
    fig_line.update_layout(yaxis2=dict(title='Volume', overlaying='y', side='right'))

st.plotly_chart(fig_line, use_container_width=True)

# Candlestick Chart
st.markdown("### Candlestick Chart")
fig_candle = go.Figure(data=[go.Candlestick(x=filtered_data['Date'],
                                             open=filtered_data['Open'],
                                             high=filtered_data['High'],
                                             low=filtered_data['Low'],
                                             close=filtered_data['Close'])])
st.plotly_chart(fig_candle, use_container_width=True)

# OHLC Chart
st.markdown("### OHLC Chart")
fig_ohlc = go.Figure(data=[go.Ohlc(x=filtered_data['Date'],
                                   open=filtered_data['Open'],
                                   high=filtered_data['High'],
                                   low=filtered_data['Low'],
                                   close=filtered_data['Close'])])
st.plotly_chart(fig_ohlc, use_container_width=True)

# Moving Average
st.sidebar.subheader("Moving Average")
window = st.sidebar.slider("Moving Average Window", min_value=2, max_value=50, value=10)
filtered_data['Close_Moving_Avg'] = filtered_data['Close'].rolling(window=window).mean()
st.markdown("### Moving Average")
fig_avg = go.Figure()
fig_avg.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Close'], mode='lines', name='Close'))
fig_avg.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Close_Moving_Avg'], mode='lines', name='Moving Average'))
fig_avg.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(fig_avg, use_container_width=True)

# Prophet Forecasting
st.header('Prophet Forecasting')
prophet_params = {
    'horizon': st.sidebar.slider('Forecast Horizon (days)', min_value=1, max_value=365, value=90),
    'growth': st.sidebar.radio('Growth', options=['linear', 'logistic']),
    'seasonality_mode': st.sidebar.radio('Seasonality Mode', options=['additive', 'multiplicative']),
    'weekly_seasonality': st.sidebar.checkbox('Weekly Seasonality', value=True),
    'monthly_seasonality': st.sidebar.checkbox('Monthly Seasonality', value=True),
    'yearly_seasonality': st.sidebar.checkbox('Yearly Seasonality', value=True),
    'holidays': st.sidebar.selectbox('Holidays Country', options=['None', 'US', 'CA', 'UK', 'FR', 'DE', 'ES', 'IT'])
}

# Display Prophet Forecasting results
forecast, fig_forecast = prophet_forecast(data, **prophet_params)
st.plotly_chart(fig_forecast, use_container_width=True)
