# Model Validation Report: Black-Scholes Option Pricing

This report summarizes the validation of a Black-Scholes option pricing framework using controlled sample data and real Goldman Sachs option market data. The focus is on what the model does, how it is validated, what results it produces, and what its limitations are.

---

## 1. Model Objective

The objective of this project is to evaluate the Black-Scholes model as a pricing and validation framework for European call and put options.

The model is used to:

- calculate theoretical option prices,
- compute option risk sensitivities known as Greeks,
- verify put-call parity,
- compare model prices with observed market midpoint prices,
- quantify pricing errors, and
- analyze how pricing errors vary across option type and moneyness.

The project is designed as a small-scale model validation workflow rather than only a formula implementation.

---

## 2. Data Used

The project uses two types of data.

### 2.1 Controlled Sample Data

A small sample dataset is used to verify the pricing logic, test benchmark Black-Scholes outputs, and confirm that the model behaves as expected under simple assumptions.

### 2.2 Goldman Sachs Option Market Data

The real-data validation uses a Goldman Sachs option-prices dataset. The dataset contains option-level market information such as:

- underlying stock price,
- strike price,
- option type,
- expiration date,
- data date,
- bid price,
- ask price,
- implied volatility,
- volume,
- open interest, and
- vendor-provided Greeks.

For each contract, the market price is approximated using the midpoint of bid and ask quotes:

```text
Market Price = (Bid + Ask) / 2
```

This midpoint is used as the observed market reference price.

---

## 3. Model Inputs

The Black-Scholes model uses the following inputs:

| Input | Meaning |
|---|---|
| `S` | Current underlying stock price |
| `K` | Strike price |
| `T` | Time to maturity in years |
| `r` | Risk-free interest rate assumption |
| `sigma` | Volatility input |
| `option_type` | Call or put |
| `market_price` | Observed market midpoint price |

For the Goldman Sachs dataset, `sigma` is taken from the implied volatility column and `market_price` is calculated from bid and ask prices.

---

## 4. Pricing Methodology

The model computes theoretical European call and put prices using the Black-Scholes closed-form pricing equations.

For a European call option, the model price is:

```text
C = S N(d1) - K exp(-rT) N(d2)
```

For a European put option, the model price is:

```text
P = K exp(-rT) N(-d2) - S N(-d1)
```

where:

```text
d1 = [ln(S/K) + (r + sigma^2 / 2)T] / [sigma sqrt(T)]
d2 = d1 - sigma sqrt(T)
```

Here, `N(.)` denotes the cumulative distribution function of the standard normal distribution.

---

## 5. Greeks and Risk Sensitivities

The model computes the main option Greeks to measure how sensitive the option value is to changes in key inputs.

| Greek | Interpretation |
|---|---|
| Delta | Sensitivity of option price to the underlying stock price |
| Gamma | Sensitivity of Delta to the underlying stock price |
| Vega | Sensitivity of option price to volatility |
| Theta | Sensitivity of option price to time decay |
| Rho | Sensitivity of option price to interest rate |

These sensitivities help evaluate the risk profile of each option and confirm that the model responds in a financially meaningful way.

---

## 6. Validation Checks

The model is validated using four main checks.

### 6.1 Benchmark Pricing Check

The model is tested on a standard benchmark case:

```text
S = 100
K = 100
T = 1
r = 0.05
sigma = 0.20
```

For this benchmark, the expected Black-Scholes prices are approximately:

```text
Call Price = 10.4506
Put Price  = 5.5735
```

Matching these values confirms that the pricing formula has been implemented correctly.

### 6.2 Put-Call Parity Check

For European options on a non-dividend-paying stock, put-call parity is:

```text
C - P = S - K exp(-rT)
```

The model calculates the parity error:

```text
Parity Error = (C - P) - [S - K exp(-rT)]
```

A parity error close to zero indicates internal consistency between the call and put pricing functions.

### 6.3 Market Price Comparison

For each option contract in the Goldman Sachs dataset, the model compares:

```text
Black-Scholes Model Price
```

with:

```text
Market Midpoint Price
```

The pricing error is calculated as:

```text
Pricing Error = Market Price - Model Price
```

This shows whether the model overprices or underprices each contract relative to the observed market quote.

### 6.4 Sensitivity Analysis

The model performs sensitivity analysis by changing one input at a time while keeping other inputs fixed.

The project analyzes sensitivity to:

- volatility,
- time to maturity, and
- strike price.

This verifies whether option prices move in economically reasonable directions when assumptions change.

---

## 7. Error Metrics

The project reports the following quantitative validation metrics:

| Metric | Meaning |
|---|---|
| MAE | Mean absolute difference between market price and model price |
| RMSE | Square root of the average squared pricing error |
| MAPE | Mean absolute percentage error |
| Average Pricing Error | Average signed pricing difference |
| Max Absolute Error | Largest absolute pricing error |

These metrics summarize the magnitude and direction of model pricing deviations.

---

## 8. Segmented Error Analysis

The real-data validation also analyzes errors by segment.

### 8.1 Error by Option Type

Errors are grouped separately for:

- call options,
- put options.

This helps determine whether the model performs differently for calls and puts.

### 8.2 Error by Moneyness

Moneyness is defined as:

```text
Moneyness = S / K
```

The project uses the following moneyness buckets:

```text
S/K < 0.95              -> OTM/Low
0.95 <= S/K <= 1.05     -> ATM
S/K > 1.05              -> ITM/High
```

This helps identify whether pricing errors are larger for out-of-the-money, at-the-money, or in-the-money contracts.

---

## 9. Visual Outputs

The project generates plots to support the validation analysis.

### 9.1 Model Price vs Market Price

This plot compares Black-Scholes model prices with market midpoint prices. Points closer to the diagonal line indicate stronger agreement between the model and market.

![Model Price vs Market Price](plots/model_vs_market_price.png)

### 9.2 Pricing Error Distribution

This plot shows the distribution of pricing errors across the real option contracts.

![Pricing Error Distribution](plots/pricing_error_distribution.png)

### 9.3 Mean Absolute Error by Moneyness Bucket

This plot shows how pricing error changes across moneyness categories.

![MAE by Moneyness Bucket](plots/mae_by_moneyness_bucket.png)

### 9.4 Volatility Sensitivity

This plot shows how call and put prices change as volatility changes.

![Volatility Sensitivity](plots/volatility_sensitivity.png)

### 9.5 Maturity Sensitivity

This plot shows how call and put prices change as time to maturity changes.

![Maturity Sensitivity](plots/maturity_sensitivity.png)

### 9.6 Strike Sensitivity

This plot shows how call and put prices change as the strike price changes.

![Strike Sensitivity](plots/strike_sensitivity.png)

---

## 10. Generated Files

The model validation workflow produces the following output files:

```text
reports/pricing_error_results.csv
reports/gs_pricing_error_results.csv
reports/gs_error_by_option_type.csv
reports/gs_error_by_moneyness.csv
reports/volatility_sensitivity.csv
reports/maturity_sensitivity.csv
reports/strike_sensitivity.csv
reports/plots/model_vs_market_price.png
reports/plots/pricing_error_distribution.png
reports/plots/mae_by_moneyness_bucket.png
reports/plots/volatility_sensitivity.png
reports/plots/maturity_sensitivity.png
reports/plots/strike_sensitivity.png
```

---

## 11. Model Assumptions

The current implementation relies on the standard Black-Scholes assumptions:

- options are European-style,
- the underlying asset pays no dividends,
- volatility is constant over the life of the option,
- the risk-free rate is constant,
- markets are frictionless,
- there are no transaction costs,
- continuous hedging is possible,
- the underlying stock price follows lognormal dynamics.

---

## 12. Important Validation Note

The real-data analysis uses implied volatility from the dataset as the volatility input. Since implied volatility is itself inferred from market option prices, the comparison between Black-Scholes model prices and market midpoint prices should mainly be interpreted as an implementation and consistency validation exercise.

It is not a fully independent forecasting test.

A stronger future version would estimate volatility from historical Goldman Sachs stock returns and then compare those historical-volatility-based prices with market option prices.

---

## 13. Limitations

The current model has the following limitations:

- dividend yield is not included,
- the risk-free rate is fixed as a simplifying assumption,
- volatility is treated as constant for each contract,
- American-style early exercise is not modeled,
- liquidity effects are not modeled,
- transaction costs are ignored,
- bid-ask spread effects are simplified using midpoint prices,
- implied volatility is used as an input, so pricing errors may appear smaller than in an independent forecasting setup.

---

## 14. Possible Extensions

The project can be extended by adding:

- dividend yield support,
- historical volatility estimation,
- implied volatility solver,
- comparison between implied-volatility and historical-volatility pricing,
- maturity-matched risk-free rates,
- Monte Carlo option pricing,
- volatility smile analysis,
- volatility surface analysis,
- Streamlit dashboard visualization.

---

## 15. Conclusion

This project implements a complete Black-Scholes pricing and model validation workflow. It does not only calculate option prices; it also checks theoretical consistency, computes risk sensitivities, compares model output with real option market data, measures pricing errors, segments those errors, and visualizes model behavior.

The framework demonstrates practical skills in derivatives pricing, quantitative finance, financial model validation, Python programming, and data-driven error analysis.