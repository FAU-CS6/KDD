import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def main():
    weather = pd.read_csv(os.path.join("data", "weather-nuremberg.csv"))
    weather.rename(
        columns={name: name.strip() for name in weather.columns.values}, inplace=True
    )
    weather.drop_duplicates(subset="MESS_DATUM", keep="first", inplace=True)
    weather.drop(labels=["QN_4", "QN_3", "STATIONS_ID"], axis=1, inplace=True)
    weather.replace(-999, np.nan, inplace=True)
    weather.dropna(axis=0, inplace=True)
    weather["MESS_DATUM"] = pd.to_datetime(weather["MESS_DATUM"].astype(str))
    weather.index = pd.DatetimeIndex(weather["MESS_DATUM"])
    weather["MONTH"] = weather.index.month
    weather["YEAR"] = weather.index.year
    date_range = pd.date_range(
        start=weather.MESS_DATUM.min(), end=weather.MESS_DATUM.max()
    )
    weather = weather.reindex(date_range)
    weather["TMK"] = weather["TMK"].interpolate(inplace=False, axis=0)
    weather = weather[["MESS_DATUM", "YEAR", "MONTH", "TMK"]]
    weather.dropna(axis=0, inplace=True)
    weather = weather.astype({"MONTH": "int32", "YEAR": "int32"})
    weather = weather.drop(weather[weather["MONTH"] == 6.5].index)

    sns.set(rc={"figure.figsize": (11.7, 5.27)})

    ax = sns.boxplot(
        x="MONTH",
        y="TMK",
        data=weather,
    )
    ax.set(
        xlabel="Month",
        ylabel="Avg. Daily Temperature in °C",
        title="Avg. Daily Temperature of Nuremberg Throughout the Years of 1955 - 2021",
    )
    sns.despine()
    plt.savefig(os.path.join("img", "weather-nuremberg-monthly-boxplot.pdf"))


if __name__ == "__main__":
    main()
