import numpy as np
import pandas as pd
import pandas_ta as ta


def SSL_channel(df, period=21):
    def get_decimal_places(number):
        number_str = str(number)
        if '.' in number_str:
            return len(number_str.split('.')[1])
        else:
            return 0

    df_copy = df.copy()
    precision = get_decimal_places(df_copy['open'].iloc[0])

    smaHigh = ta.sma(df_copy['high'], length=period)
    smaLow = ta.sma(df_copy['low'], length=period)

    Hlv = np.where(df_copy['close'] > smaHigh, 1, np.where(df_copy['close'] < smaLow, -1, np.nan))
    Hlv = pd.Series(Hlv, index=df_copy.index).ffill()

    sslDown = np.where(Hlv < 0, smaHigh, smaLow)
    sslUp = np.where(Hlv < 0, smaLow, smaHigh)
    df_copy.loc[:, 'sslUp'] = np.round(sslUp, precision)
    df_copy.loc[:, 'sslDown'] = np.round(sslDown, precision)

    crossover_up = (df_copy['sslUp'] > df_copy['sslDown']) & (df_copy['sslUp'].shift(1) < df_copy['sslDown'].shift(1))
    crossover_down = (df_copy['sslUp'] < df_copy['sslDown']) & (df_copy['sslUp'].shift(1) > df_copy['sslDown'].shift(1))
    df_copy.loc[:, 'crossover_signal'] = np.where(crossover_up, 1, np.where(crossover_down, -1, 0))

    # Add new columns
    df_copy['previous_sslUp'] = df_copy['sslUp'].shift(1).where(df_copy['crossover_signal'].isin([1,-1]), 0)
    df_copy['previous_sslDown'] = df_copy['sslDown'].shift(1).where(df_copy['crossover_signal'].isin([1,-1]), 0)
    df_copy['current_sslUp'] = df_copy['sslUp'].where(df_copy['crossover_signal'].isin([1,-1]), 0)
    df_copy['current_sslDown'] = df_copy['sslDown'].where(df_copy['crossover_signal'].isin([1,-1]), 0)

    return df_copy









