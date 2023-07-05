import pandas as pd

import indicators


def getData():
    df = pd.read_csv('data/EURUSD_1Min.csv')
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'Volume']
    df = df.drop(columns='Volume')
    df['timestamp'] = df['timestamp'].str.replace(' GMT+0530', '')
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d.%m.%Y %H:%M:%S.%f')

    # Localize the 'timestamp' column to 'Asia/Kolkata' but don't convert to UTC
    df['timestamp'] = df['timestamp'].dt.tz_localize('Asia/Kolkata')

    df.set_index('timestamp', inplace=True)
    return df


def sslExperiments(df):
    mask = (df['open'] == df['high']) & (df['high'] == df['low']) & (df['low'] == df['close'])
    df = df[~mask]
    sslData = indicators.SSL_channel(df, period=3)
    sslData = sslData.dropna()
    print(sslData.tail())

    sslData.to_csv('data/ssl_data.csv')
    pass


if __name__ == '__main__':
    data = getData()
    sslExperiments(data)
