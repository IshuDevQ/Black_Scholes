import os
import matplotlib.pyplot as plt
import pandas as pd

from src.black_scholes import BlackScholesModel
from src.greeks import GreeksCalculator
from src.validation import put_call_parity_check, pricing_error_analysis
from src.sensitivity import sensitivity_analysis
from src.data_loader import load_gs_options_data


def save_line_plot(df, x_col, y_cols, title, xlabel, ylabel, output_path):
    """
    Saves a simple line plot for sensitivity analysis results.
    """
    plt.figure(figsize=(8, 5))

    for y_col in y_cols:
        plt.plot(df[x_col], df[y_col], marker="o", label=y_col)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_real_data_plots(result):
    """
    Saves plots for real-market option pricing validation.
    """
    os.makedirs("reports/plots", exist_ok=True)

    plt.figure(figsize=(6, 6))
    plt.scatter(result["market_price"], result["model_price"], alpha=0.6)
    min_price = min(result["market_price"].min(), result["model_price"].min())
    max_price = max(result["market_price"].max(), result["model_price"].max())
    plt.plot([min_price, max_price], [min_price, max_price], linestyle="--")
    plt.title("Model Price vs Market Price")
    plt.xlabel("Market Mid Price")
    plt.ylabel("Black-Scholes Model Price")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("reports/plots/model_vs_market_price.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(result["pricing_error"], bins=30, edgecolor="black")
    plt.title("Distribution of Pricing Errors")
    plt.xlabel("Pricing Error = Market Price - Model Price")
    plt.ylabel("Frequency")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("reports/plots/pricing_error_distribution.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8, 5))
    bucket_mae = result.groupby("moneyness_bucket", observed=False)["absolute_error"].mean()
    bucket_mae.plot(kind="bar")
    plt.title("Mean Absolute Error by Moneyness Bucket")
    plt.xlabel("Moneyness Bucket")
    plt.ylabel("Mean Absolute Error")
    plt.xticks(rotation=0)
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("reports/plots/mae_by_moneyness_bucket.png", dpi=300)
    plt.close()

def run_single_option_example():
    print("\n==============================")
    print("Single Option Pricing Example")
    print("==============================")

    model = BlackScholesModel(
        S=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.20,
    )

    greeks = GreeksCalculator(model)
    parity = put_call_parity_check(model)

    print(f"d1: {model.d1():.6f}")
    print(f"d2: {model.d2():.6f}")
    print(f"Call Price: {model.call_price():.6f}")
    print(f"Put Price: {model.put_price():.6f}")

    print("\nGreeks")
    print("------")
    print(f"Call Delta: {greeks.call_delta():.6f}")
    print(f"Put Delta: {greeks.put_delta():.6f}")
    print(f"Gamma: {greeks.gamma():.6f}")
    print(f"Vega: {greeks.vega():.6f}")
    print(f"Call Theta per day: {greeks.call_theta():.6f}")
    print(f"Put Theta per day: {greeks.put_theta():.6f}")
    print(f"Call Rho: {greeks.call_rho():.6f}")
    print(f"Put Rho: {greeks.put_rho():.6f}")

    print("\nPut-Call Parity Check")
    print("---------------------")
    print(f"C - P: {parity['left_side_C_minus_P']:.10f}")
    print(f"S - K exp(-rT): {parity['right_side_S_minus_discounted_K']:.10f}")
    print(f"Parity Error: {parity['parity_error']:.12f}")
    print(f"Parity Pass: {parity['parity_pass']}")


def run_market_price_comparison():
    print("\n==============================")
    print("Market Price Comparison")
    print("==============================")

    df = pd.read_csv("data/sample_options.csv")

    result, metrics = pricing_error_analysis(df)

    print("\nPricing Error Table")
    print("-------------------")
    print(result.round(4).to_string(index=False))

    print("\nError Metrics")
    print("-------------")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.6f}")

    os.makedirs("reports", exist_ok=True)
    result.to_csv("reports/pricing_error_results.csv", index=False)

def run_gs_real_data_analysis():
    print("\n==============================")
    print("Goldman Sachs Real Options Data Analysis")
    print("==============================")

    df = load_gs_options_data("data/gs_option_prices.csv")

    print(f"\nCleaned dataset shape: {df.shape}")
    print("\nCleaned data sample:")
    print(df.head().round(4).to_string(index=False))

    result, metrics = pricing_error_analysis(df)

    print("\nReal Data Pricing Error Table")
    print("-----------------------------")
    print(result.round(4).head(20).to_string(index=False))

    print("\nReal Data Error Metrics")
    print("-----------------------")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.6f}")

    print("\nError Metrics by Option Type")
    print("----------------------------")
    option_type_summary = (
        result.groupby("option_type")
        .agg(
            contracts=("option_type", "count"),
            avg_market_price=("market_price", "mean"),
            avg_model_price=("model_price", "mean"),
            mae=("absolute_error", "mean"),
            rmse=("pricing_error", lambda x: (x.pow(2).mean()) ** 0.5),
            avg_percentage_error=("percentage_error", "mean"),
        )
        .reset_index()
    )
    print(option_type_summary.round(4).to_string(index=False))

    result["moneyness"] = result["S"] / result["K"]
    result["moneyness_bucket"] = pd.cut(
        result["moneyness"],
        bins=[0, 0.95, 1.05, float("inf")],
        labels=["OTM/Low", "ATM", "ITM/High"],
    )

    print("\nError Metrics by Moneyness Bucket")
    print("---------------------------------")
    moneyness_summary = (
        result.groupby("moneyness_bucket", observed=False)
        .agg(
            contracts=("moneyness_bucket", "count"),
            avg_moneyness=("moneyness", "mean"),
            mae=("absolute_error", "mean"),
            rmse=("pricing_error", lambda x: (x.pow(2).mean()) ** 0.5),
            avg_percentage_error=("percentage_error", "mean"),
        )
        .reset_index()
    )
    print(moneyness_summary.round(4).to_string(index=False))

    os.makedirs("reports", exist_ok=True)
    result.to_csv("reports/gs_pricing_error_results.csv", index=False)
    option_type_summary.to_csv("reports/gs_error_by_option_type.csv", index=False)
    moneyness_summary.to_csv("reports/gs_error_by_moneyness.csv", index=False)

    save_real_data_plots(result)
    print("\nSaved real-data plots to reports/plots/")

def run_sensitivity_examples():
    print("\n==============================")
    print("Sensitivity Analysis")
    print("==============================")

    base_params = {
        "S": 100,
        "K": 100,
        "T": 1,
        "r": 0.05,
        "sigma": 0.20,
    }

    volatility_values = [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    maturity_values = [0.25, 0.50, 1.00, 1.50, 2.00]
    strike_values = [80, 90, 100, 110, 120]

    vol_result = sensitivity_analysis(base_params, "sigma", volatility_values)
    maturity_result = sensitivity_analysis(base_params, "T", maturity_values)
    strike_result = sensitivity_analysis(base_params, "K", strike_values)

    print("\nVolatility Sensitivity")
    print("----------------------")
    print(vol_result.round(4).to_string(index=False))

    print("\nMaturity Sensitivity")
    print("--------------------")
    print(maturity_result.round(4).to_string(index=False))

    print("\nStrike Sensitivity")
    print("------------------")
    print(strike_result.round(4).to_string(index=False))

    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/plots", exist_ok=True)

    vol_result.to_csv("reports/volatility_sensitivity.csv", index=False)
    maturity_result.to_csv("reports/maturity_sensitivity.csv", index=False)
    strike_result.to_csv("reports/strike_sensitivity.csv", index=False)

    save_line_plot(
        vol_result,
        x_col="sigma",
        y_cols=["call_price", "put_price"],
        title="Option Price Sensitivity to Volatility",
        xlabel="Volatility",
        ylabel="Option Price",
        output_path="reports/plots/volatility_sensitivity.png",
    )

    save_line_plot(
        maturity_result,
        x_col="T",
        y_cols=["call_price", "put_price"],
        title="Option Price Sensitivity to Maturity",
        xlabel="Time to Maturity in Years",
        ylabel="Option Price",
        output_path="reports/plots/maturity_sensitivity.png",
    )

    save_line_plot(
        strike_result,
        x_col="K",
        y_cols=["call_price", "put_price"],
        title="Option Price Sensitivity to Strike Price",
        xlabel="Strike Price",
        ylabel="Option Price",
        output_path="reports/plots/strike_sensitivity.png",
    )

    print("\nSaved sensitivity plots to reports/plots/")


def main():
    run_single_option_example()
    run_market_price_comparison()
    run_sensitivity_examples()

    try:
        run_gs_real_data_analysis()
    except FileNotFoundError:
        print("\nSkipping GS real-data analysis: data/gs_option_prices.csv not found.")

    
if __name__ == "__main__":
    main()