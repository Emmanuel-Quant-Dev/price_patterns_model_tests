from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

def stochastic_analysis(file):

    
    stock_file = f"list_of_stocks/stocks/{file}"

    df = pd.read_csv(stock_file)

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date").reset_index(drop=True)


    PRICE_COLUMN = "Adj Close"



    df["Simple_Return"] = (
        df[PRICE_COLUMN]
        .pct_change()
    )

    df["Simple_Return_Pct"] = (
        df["Simple_Return"] * 100
    )


  
    #  Applying LOG manipulations


    df["Log_Return"] = np.log(
        df[PRICE_COLUMN]
        / df[PRICE_COLUMN].shift(1)
    )

    df["Log_Return_Pct"] = (
        df["Log_Return"] * 100
    )

    # Approximate number of US trading days per year
    TRADING_DAYS = 252


    # applying ROLLING VOLATILITY


    df["Rolling_Volatility_20"] = (
        df["Log_Return"]
        .rolling(window=20)
        .std()
        * np.sqrt(TRADING_DAYS)
    )


    df["Rolling_Volatility_50"] = (
        df["Log_Return"]
        .rolling(window=50)
        .std()
        * np.sqrt(TRADING_DAYS)
    )


    df["Rolling_Volatility_252"] = (
        df["Log_Return"]
        .rolling(window=252)
        .std()
        * np.sqrt(TRADING_DAYS)
    )


    # Convert to percentage
    df["Rolling_Volatility_20_Pct"] = (
        df["Rolling_Volatility_20"] * 100
    )

    df["Rolling_Volatility_50_Pct"] = (
        df["Rolling_Volatility_50"] * 100
    )

    df["Rolling_Volatility_252_Pct"] = (
        df["Rolling_Volatility_252"] * 100
    )

    # Average log return over previous 20 observations

    df["Rolling_Drift_20"] = (
        df["Log_Return"]
        .rolling(window=20)
        .mean()
    )


    df["Rolling_Drift_50"] = (
        df["Log_Return"]
        .rolling(window=50)
        .mean()
    )


    # Annualised drift approximation

    df["Annualised_Drift_20"] = (
        df["Rolling_Drift_20"]
        * TRADING_DAYS
    )

    df["Annualised_Drift_50"] = (
        df["Rolling_Drift_50"]
        * TRADING_DAYS
    )

    rolling_mean_20 = (
        df[PRICE_COLUMN]
        .rolling(window=20)
        .mean()
    )

    rolling_std_20 = (
        df[PRICE_COLUMN]
        .rolling(window=20)
        .std()
    )


    df["Price_ZScore_20"] = (
        (
            df[PRICE_COLUMN]
            - rolling_mean_20
        )
        / rolling_std_20
    )


    # Very simple interpretation:
    #
    # Z > 2   = unusually high
    # Z < -2  = unusually low
    #
    # This is NOT automatically a buy/sell signal.
    # It identifies observations worth investigating.

    df["Mean_Reversion_State"] = np.select(
        [
            df["Price_ZScore_20"] >= 2,
            df["Price_ZScore_20"] <= -2
        ],
        [
            "Above Normal Range",
            "Below Normal Range"
        ],
        default="Normal"
    )



    df["Price_Change"] = (
        df[PRICE_COLUMN]
        .diff()
    )


    df["Squared_Log_Return"] = (
        df["Log_Return"] ** 2
    )




    df["YearMonth"] = (
        df["Date"]
        .dt
        .to_period("M")
    )



    monthly_stochastic_stats = (
        df.groupby("YearMonth")
        .agg(
            Mean_Return=(
                "Log_Return",
                "mean"
            ),

            Median_Return=(
                "Log_Return",
                "median"
            ),

            Return_Std=(
                "Log_Return",
                "std"
            ),

            Return_Variance=(
                "Log_Return",
                "var"
            ),

            Min_Return=(
                "Log_Return",
                "min"
            ),

            Max_Return=(
                "Log_Return",
                "max"
            ),

            Mean_Price=(
                PRICE_COLUMN,
                "mean"
            ),

            Price_Std=(
                PRICE_COLUMN,
                "std"
            ),

            Mean_ZScore=(
                "Price_ZScore_20",
                "mean"
            ),

            Mean_Squared_Return=(
                "Squared_Log_Return",
                "mean"
            )
        )
    )



    #  monthly volatility annualised

    monthly_stochastic_stats[
        "Annualised_Volatility"
    ] = (
        monthly_stochastic_stats["Return_Std"]
        * np.sqrt(TRADING_DAYS)
    )


    monthly_stochastic_stats[
        "Annualised_Volatility_Pct"
    ] = (
        monthly_stochastic_stats[
            "Annualised_Volatility"
        ]
        * 100
    )

    monthly_stochastic_stats[
        "Annualised_Mean_Return"
    ] = (
        monthly_stochastic_stats[
            "Mean_Return"
        ]
        * TRADING_DAYS
    )


    #  Geometric brownian motion parameters


    clean_returns = (
        df["Log_Return"]
        .dropna()
    )

    mu = clean_returns.mean()

    sigma = clean_returns.std()


    annual_mu = (
        mu * TRADING_DAYS
    )

    annual_sigma = (
        sigma * np.sqrt(TRADING_DAYS)
    )


    print(
        "Daily mean log return:",
        mu
    )

    print(
        "Daily volatility:",
        sigma
    )

    print(
        "Annualised drift:",
        annual_mu
    )

    print(
        "Annualised volatility:",
        annual_sigma
    )


    # Geometric brownian motion parameters with use of monte carlo


    def simulate_gbm(
        starting_price,
        mu,
        sigma,
        days=252,
        simulations=1000
    ):

        dt = 1 / TRADING_DAYS

        results = np.zeros(
            (
                days + 1,
                simulations
            )
        )

        results[0] = starting_price

        for t in range(
            1,
            days + 1
        ):

            random_shock = np.random.normal(
                0,
                1,
                simulations
            )

            results[t] = (
                results[t - 1]
                * np.exp(
                    (
                        mu
                        - 0.5
                        * sigma ** 2
                    )
                    * dt
                    +
                    sigma
                    * np.sqrt(dt)
                    * random_shock
                )
            )

        return results



    last_price = (
        df[PRICE_COLUMN]
        .dropna()
        .iloc[-1]
    )


    simulation = simulate_gbm(
        starting_price=last_price,
        mu=annual_mu,
        sigma=annual_sigma,
        days=252,
        simulations=1000
    )


    # MONTE CARLO RESULTS Monte carlo results


    final_prices = simulation[-1]


    monte_carlo_summary = pd.DataFrame(
        {
            "Statistic": [
                "Starting Price",
                "Mean Final Price",
                "Median Final Price",
                "Minimum Final Price",
                "Maximum Final Price",
                "5th Percentile",
                "25th Percentile",
                "75th Percentile",
                "95th Percentile"
            ],

            "Value": [
                last_price,
                np.mean(final_prices),
                np.median(final_prices),
                np.min(final_prices),
                np.max(final_prices),
                np.percentile(
                    final_prices,
                    5
                ),
                np.percentile(
                    final_prices,
                    25
                ),
                np.percentile(
                    final_prices,
                    75
                ),
                np.percentile(
                    final_prices,
                    95
                )
            ]
        }
    )


    probability_above = np.mean(
        final_prices
        > last_price
    )


    probability_below = np.mean(
        final_prices
        < last_price
    )


    probability_summary = pd.DataFrame(
        {
            "Metric": [
                "Probability Above Starting Price",
                "Probability Below Starting Price"
            ],

            "Probability": [
                probability_above,
                probability_below
            ]
        }
    )

    simulation_df = pd.DataFrame(
        simulation
    )

    simulation_df.index.name = (
        "Trading_Day"
    )



    # save results to results directory for further processing
  

    df.to_csv(
        "AA_stochastic_analysis.csv",
        index=False
    )
    monthly_stochastic_stats.to_csv(
        f"results/{file}_AA_monthly_stochastic_statistics.csv"
    )
    monte_carlo_summary.to_csv(
        f"results/{file}_AA_monte_carlo_summary.csv",
        index=False
    )
    probability_summary.to_csv(
       f"results/{file}_AA_probability_summary.csv",
        index=False
    )
    simulation_df.to_csv(
        f"results/{file}_AA_gbm_simulations.csv"
    )


#a = stochastic_analyis("AAT.csv")