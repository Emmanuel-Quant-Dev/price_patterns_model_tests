import pandas as pd
from pathlib import Path
#PROJECT_ROOT = Path(__file__).resolve().parent.parent


def move_avg_info_gathering(file):
    """
    This script is to gather the initial information of the entered stock.
    It will retrieve information relating to monthly price ranges, monthly returns and
    monthly stats of the data - ranging from mean to count and std.

    """
        
    df = pd.read_csv(f"list_of_stocks/stocks/{file}")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume"
    ]

    df["YearMonth"] = df["Date"].dt.to_period("M")


    for column in columns:

        df[f"{column}_MA20"] = (
            df[column]
            .rolling(window=20)
            .mean()
        )

        df[f"{column}_MA50"] = (
            df[column]
            .rolling(window=50)
            .mean()
        )

        df[f"{column}_MA200"] = (
            df[column]
            .rolling(window=200)
            .mean()
        )


    # Obtaining the monthly statistics 
    
    monthly_stats = (
        df.groupby("YearMonth")[columns]
        .agg([
            "mean",
            "median",
            "std",
            "var",
            "min",
            "max",
            "count"
        ])
    )

    # obtaining daily returns of file   

    df["Daily_Return"] = df["Adj Close"].pct_change()

    df["Daily_Return_Pct"] = (
        df["Daily_Return"] * 100
    )


    monthly_return_stats = (
        df.groupby("YearMonth")["Daily_Return"]
        .agg([
            "mean",
            "median",
            "std",
            "min",
            "max",
            "count"
        ])
    )

    # Obtain monthly price range

    monthly_price_range = (
        df.groupby("YearMonth")
        .agg(
            Monthly_High=("High", "max"),
            Monthly_Low=("Low", "min"),
            Average_Close=("Close", "mean"),
            Median_Close=("Close", "median"),
            Average_Volume=("Volume", "mean")
        )
    )

    monthly_price_range["Price_Range"] = (
        monthly_price_range["Monthly_High"]
        -
        monthly_price_range["Monthly_Low"]
    )


    #Save items analysed to results table for further processing

    df.to_csv(
        f"results/{file}_quant_analysis.csv",
        index=False
    )

    monthly_stats.to_csv(
        f"results/{file}_monthly_statistics.csv"
    )

    monthly_return_stats.to_csv(
        f"results/{file}_monthly_return_statistics.csv"
    )

    monthly_price_range.to_csv(
        f"results/{file}_monthly_price_range.csv"
    )

#a = move_avg_info_gathering("AAT.csv")
