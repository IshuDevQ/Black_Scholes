import pandas as pd


def load_gs_options_data(file_path: str) -> pd.DataFrame:
    """
    Loads and cleans the Goldman Sachs options dataset.

    Converts the Kaggle dataset into the standard format required by
    the Black-Scholes validation framework.

    Final columns:
    S, K, T, r, sigma, option_type, market_price
    """

    df = pd.read_csv(file_path)

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Convert dates
    df["DataDate"] = pd.to_datetime(df["DataDate"])
    df["Expiration"] = pd.to_datetime(df["Expiration"])

    # Time to maturity in years
    df["T"] = (df["Expiration"] - df["DataDate"]).dt.days / 365

    # Market midpoint price
    df["market_price"] = (df["Bid"] + df["Ask"]) / 2

    # Standardized dataframe for pricing engine
    clean = pd.DataFrame(
        {
            "S": df["UnderlyingPrice"],
            "K": df["Strike"],
            "T": df["T"],
            "r": 0.05,  # fixed assumption for now
            "sigma": df["IVMean"],
            "option_type": df["Type"].str.lower(),
            "market_price": df["market_price"],
            "bid": df["Bid"],
            "ask": df["Ask"],
            "last": df["Last"],
            "volume": df["Volume"],
            "open_interest": df["OpenInterest"],
            "market_delta": df["Delta"],
            "market_gamma": df["Gamma"],
            "market_theta": df["Theta"],
            "market_vega": df["Vega"],
        }
    )

    # Basic cleaning
    clean = clean.dropna()

    clean = clean[
        (clean["S"] > 0)
        & (clean["K"] > 0)
        & (clean["T"] > 0)
        & (clean["sigma"] > 0)
        & (clean["market_price"] > 0)
        & (clean["bid"] >= 0)
        & (clean["ask"] > 0)
        & (clean["ask"] >= clean["bid"])
    ]

    clean = clean[clean["option_type"].isin(["call", "put"])]

    return clean.reset_index(drop=True)