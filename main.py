import numpy as np
import pandas as pd
import math
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


def calculate_angle(p1, p2, p3):
    a = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    b = np.sqrt((p3[0] - p1[0]) ** 2 + (p3[1] - p1[1]) ** 2)
    c = np.sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2)

    # Check if any side length is 0
    if a == 0 or b == 0:
        return np.nan  # or return any other appropriate value

    # Calculate the cosine of the angle between a and b
    cos_c = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)

    # Check if cos_c is out of range
    if cos_c < -1 or cos_c > 1:
        return np.nan  # or return any other appropriate value

    # Calculate the angle in degrees
    theta = np.arccos(cos_c) * 180 / np.pi

    return theta


def sslExperiments(df):
    sslData = indicators.SSL_channel(df, period=3)
    sslData = sslData.dropna()
    sslData = sslData[sslData['crossover_signal'] != 0]
    cols_to_remove = ['open', 'high', 'low', 'close', 'sslUp', 'sslDown', 'crossover_signal']
    sslData = sslData.drop(columns=cols_to_remove)
    # Convert timestamp to numerical values (Unix timestamp) for calculations
    # Define the points (A, B, C, D)
    A = sslData['previous_sslUp_A']
    B = sslData['current_sslDown_B']
    C = sslData['current_sslUp_C']
    D = sslData['previous_sslDown_D']

    # Convert each column to a 1D numpy array
    A = A.to_numpy()
    B = B.to_numpy()
    C = C.to_numpy()
    D = D.to_numpy()

    # Calculate angles for each triangle and add them to the dataframe
    # Angles for Triangle ADC
    sslData['Angle_A_ADC'] = [calculate_angle((A[i], 0), (D[i], 0), (C[i], 0)) for i in range(len(A))]
    sslData['Angle_D_ADC'] = [calculate_angle((D[i], 0), (A[i], 0), (C[i], 0)) for i in range(len(A))]
    sslData['Angle_C_ADC'] = [calculate_angle((C[i], 0), (A[i], 0), (D[i], 0)) for i in range(len(A))]

    # Angles for Triangle BDC
    sslData['Angle_B_BDC'] = [calculate_angle((B[i], 0), (D[i], 0), (C[i], 0)) for i in range(len(A))]
    sslData['Angle_D_BDC'] = [calculate_angle((D[i], 0), (B[i], 0), (C[i], 0)) for i in range(len(A))]
    sslData['Angle_C_BDC'] = [calculate_angle((C[i], 0), (B[i], 0), (D[i], 0)) for i in range(len(A))]

    # Angles for Triangle ABD
    sslData['Angle_A_ABD'] = [calculate_angle((A[i], 0), (B[i], 0), (D[i], 0)) for i in range(len(A))]
    sslData['Angle_B_ABD'] = [calculate_angle((B[i], 0), (A[i], 0), (D[i], 0)) for i in range(len(A))]
    sslData['Angle_D_ABD'] = [calculate_angle((D[i], 0), (A[i], 0), (B[i], 0)) for i in range(len(A))]

    # Angles for Triangle ABC
    sslData['Angle_A_ABC'] = [calculate_angle((A[i], 0), (B[i], 0), (C[i], 0)) for i in range(len(A))]
    sslData['Angle_B_ABC'] = [calculate_angle((B[i], 0), (A[i], 0), (C[i], 0)) for i in range(len(A))]
    sslData['Angle_C_ABC'] = [calculate_angle((C[i], 0), (A[i], 0), (B[i], 0)) for i in range(len(A))]

    # angle_cols = [col for col in sslData.columns if 'Angle' in col]
    # sslData[angle_cols] = sslData[angle_cols].round(5)
    #
    # for col in sslData.columns:
    #     if 'Angle' in col:
    #         sslData[col] = sslData[col].map('{:.5f}'.format)

    sslData.to_csv('data/prepared_data.csv')

    return sslData


if __name__ == '__main__':
    data = getData()
    sslExperiments(data)
