import numpy as np
import pandas as pd
from pathlib import Path

def getAndCleanPrecip():
    r = np.random.randn()

    # data came from https://www.ncdc.noaa.gov/cdo-web/datatools/lcd
    # https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf
    df = pd.read_csv('/Users/marisa/git/practice/data/Middlesex_Daily_10yr.csv')
    keysIwant = [s for s in df.keys() if 'Precip' in s]
    col = 'DailyPrecipitation'
    df[(df[col]=="T") | (df[col]=="Ts")] = "0.0"

    mySeries = df[pd.notna(df[col])][col]
    df2 = mySeries.str.extract(r'([0-9.]*)([a-zA-Z]*)', expand=True)
    df2 = df2.rename(index=str, columns={0: "precipNum", 1: "precipFlag"})
    df2['precipNum'] = df2['precipNum'].astype('float64')
    return df2

def baseProjectDir():
    return Path(__file__).resolve()

if __name__== "__main__":
    getAndCleanPrecip()
