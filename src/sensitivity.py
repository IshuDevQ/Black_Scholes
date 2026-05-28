import pandas as pd
from src.black_scholes import BlackScholesModel


def sensitivity_analysis(
    base_params: dict,
    variable_name: str,
    variable_values: list[float],
) -> pd.DataFrame:
    """
    Varies one input parameter and calculates call and put prices.

    Example:
    sensitivity_analysis(base_params, "sigma", [0.10, 0.20, 0.30])
    """

    rows = []

    for value in variable_values:
        params = base_params.copy()
        params[variable_name] = value

        model = BlackScholesModel(**params)

        rows.append(
            {
                variable_name: value,
                "call_price": model.call_price(),
                "put_price": model.put_price(),
            }
        )

    return pd.DataFrame(rows)