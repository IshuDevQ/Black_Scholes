import math
import numpy as np
import pandas as pd
from src.black_scholes import BlackScholesModel


def put_call_parity_check(model: BlackScholesModel) -> dict:
    """
    Checks put-call parity:

        C - P = S - K e^(-rT)

    Returns parity error.
    """

    call = model.call_price()
    put = model.put_price()

    left_side = call - put
    right_side = model.S - model.K * math.exp(-model.r * model.T)

    parity_error = left_side - right_side

    return {
        "call_price": call,
        "put_price": put,
        "left_side_C_minus_P": left_side,
        "right_side_S_minus_discounted_K": right_side,
        "parity_error": parity_error,
        "parity_pass": abs(parity_error) < 1e-8,
    }


def pricing_error_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Compares Black-Scholes theoretical prices with market prices.

    Required columns:
    S, K, T, r, sigma, option_type, market_price
    """

    model_prices = []

    for _, row in df.iterrows():
        model = BlackScholesModel(
            S=row["S"],
            K=row["K"],
            T=row["T"],
            r=row["r"],
            sigma=row["sigma"],
        )

        if row["option_type"].lower() == "call":
            model_price = model.call_price()
        elif row["option_type"].lower() == "put":
            model_price = model.put_price()
        else:
            raise ValueError("option_type must be either 'call' or 'put'.")

        model_prices.append(model_price)

    result = df.copy()
    result["model_price"] = model_prices
    result["pricing_error"] = result["market_price"] - result["model_price"]
    result["absolute_error"] = result["pricing_error"].abs()
    result["percentage_error"] = (result["pricing_error"] / result["market_price"]) * 100

    mae = result["absolute_error"].mean()
    rmse = np.sqrt((result["pricing_error"] ** 2).mean())
    mape = result["percentage_error"].abs().mean()

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "Average Pricing Error": result["pricing_error"].mean(),
        "Max Absolute Error": result["absolute_error"].max(),
    }

    return result, metrics