import yfinance as yf
import plotly.graph_objects as go
import plotly.subplots
from ta.trend import MACD
from ta.momentum import StochasticOscillator


yf.pdr_override()


user_input = input("Please enter a ticker: ")


df = yf.download(tickers=user_input,period='1d',interval='1m')



macd = MACD(close=df['Close'],
            window_slow=26,
            window_fast=12,
            window_sign=9)

stoch = StochasticOscillator(high=df['High'],
                             close=df['Close'],
                             low=df['Low'],
                             window=14,
                             smooth_window=3)



df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()



fig = go.Figure()


fig = plotly.subplots.make_subplots(rows=4, cols=1,
            shared_xaxes=True, vertical_spacing=0.01, row_heights=
            [0.5,0.1,0.2,0.2])


fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'], name= 'market data'))

fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA5'],
                         opacity=0.7,
                         line=dict(color='blue',width=2),
                         name='MA 5'
                         ))

fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA20'],
                         opacity=0.7,
                         line=dict(color='orange',width=2),
                         name='MA 20'))

fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume']
                     ), row=2, col=1)

fig.add_trace(go.Bar(x=df.index,
                     y=macd.macd_diff()
                     ), row=3, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=macd.macd(),
                         line=dict(color='black', width=2)
                         ), row=3, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=macd.macd_signal(),
                         line=dict(color='blue',width=1)
                         ), row=3, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=stoch.stoch(),
                         line=dict(color='black', width=1)
                         ), row=4, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=stoch.stoch_signal(),
                         line=dict(color='blue', width=1)
                         ), row=4, col=1)


fig.update_layout(
    height=900,
    width=1200,
    showlegend=False,
    xaxis_rangeslider_visible=False)



fig.update_layout(
    title=str(user_input)+' Live Share Price:',
    yaxis_title='Stock Price (USD per shares)'
)


fig.update_yaxes(title_text='Price',row=1,col=1)
fig.update_yaxes(title_text='Volume',row=2,col=1)
fig.update_yaxes(title_text='MACD',showgrid=False,row=3,col=1)
fig.update_yaxes(title_text='Stoch',row=4,col=1)


fig.update_xaxes(
    rangeslider_visible=False,
    rangeselector_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=15,label='15m',step='minute',stepmode='backward'),
            dict(count=45,label='45m',step='minute',stepmode='backward'),
            dict(count=1,label='HTD',step='hour',stepmode='todate'),
            dict(count=3,label='3h',step='hour',stepmode='backward'),
            dict(step='all')
        ])
    )
)

fig.show()