import pandas as pd
import altair as alt
import yfinance as yf
import streamlit as st

st.title('米国株化可視化アプリ')

st.sidebar.write("""
  # 株価

  こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
  """)

st.sidebar.write("""
  # 表示日数選択
  """)
# daysにはインタラクティブに変更した値が入ってくる
days = st.sidebar.slider('日数', 1, 100, 20)

st.write(f"""
  # 過去 **{days}日間** の株価
  """)

# 株価をYahoo!ファイナンスから取ってきてデータフレームに入れる関数
@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df


# try:
st.sidebar.write("""
# 株価の範囲指定
""")

# ymin ymaxにはインタラクティブに変更した値が入ってくる
ymin, ymax = st.sidebar.slider('範囲を指定ください', 0, 3000, (0, 3000))

# 取得したい株のティッカー情報
tickers = {
    'VYM': 'VYM',
    'VT': 'VT',
    'VTI': 'VTI',
    'SPYD': 'SPYD',
    'HDV': 'HDV',
    'VOO': 'VOO',
    'apple': 'AAPL',
    'meta': 'META',
    'google': 'GOOGL',
    'miclosoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN',
    'disney': 'DIS'

}

df = get_data(days, tickers)

companies = st.multiselect(
    '銘柄を選択してください。',
    list(df.index),
    ['VYM', 'HDV', 'SPYD']
)

if not companies:
    st.error('少なくとも1銘柄は選んでください。')
else:
    data = df.loc[companies]
    st.write("### 株価(USD)", data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=['index']).rename(
        columns={'value': 'stock prices(USD)', 'index': 'Date'}
    )
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("stock prices(USD):Q", stack=None,
                    scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )
    st.altair_chart(chart, use_container_width=True)
# except:
#     st.error("おっと！何かエラーが起きているようです・・・")
