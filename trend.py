import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Download the stock data for ITC from Yahoo Finance
ticker = st.sidebar.text_input('Symbol Code' ,'GAIL.NS')
data = yf.download(ticker, period='max')
data = data.reset_index()

# Extract the year from the date and group the data by year
data['Year'] = data['Date'].dt.year

# Define a function to calculate the percentage change for a given column
def percentage_change(dataframe, column):
    max_value = dataframe[column].max()
    min_value = dataframe[column].min()
    return ((max_value - min_value) / min_value) * 100

# Loop through each year and create a Plotly figure for the data
unique_years = data['Year'].unique()

for year in unique_years:
    df = data[data['Year'] == year]
    df['trend'] = df['Adj Close'].diff()

    # Calculate the percentage change for the 'Adj Close' column
    pct_change = percentage_change(df, 'Adj Close')

    # Create a Plotly figure
    fig = go.Figure()

    for i in range(1, len(df)):
        color = 'green' if df['trend'].iloc[i] > 0 else 'red'
        fig.add_trace(go.Scatter(x=df['Date'].iloc[i-1:i+1],
                                 y=df['Adj Close'].iloc[i-1:i+1],
                                 mode='lines',
                                 line=dict(color=color),
                                 showlegend=False))

    fig.update_layout(
        title=f'Close Trend Over Time - {year} (Pct Change: {pct_change:.2f}%)',
        xaxis_title='Date',
        yaxis_title='Close',
        xaxis=dict(tickangle=45),
        template='plotly_white'
    )
    # Add range slider for interactivity
    fig.update_layout(xaxis_rangeslider_visible=True)
    fig.update_layout(width=2000, height=720, plot_bgcolor='white')


    st.plotly_chart(fig)
