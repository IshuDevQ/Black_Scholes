import math
from scipy.stats import norm
from src.black_scholes import BlackScholesModel


class GreeksCalculator:
    """
    Computes option Greeks for the Black-Scholes model.
    """

    def __init__(self, model: BlackScholesModel):
        self.model = model

    def call_delta(self) -> float:
        return norm.cdf(self.model.d1())

    def put_delta(self) -> float:
        return norm.cdf(self.model.d1()) - 1

    def gamma(self) -> float:
        d1 = self.model.d1()
        S = self.model.S
        sigma = self.model.sigma
        T = self.model.T

        return norm.pdf(d1) / (S * sigma * math.sqrt(T))

    def vega(self) -> float:
        d1 = self.model.d1()
        S = self.model.S
        T = self.model.T

        # Divided by 100 to represent change per 1 percentage point volatility move
        return (S * norm.pdf(d1) * math.sqrt(T)) / 100

    def call_theta(self) -> float:
        d1 = self.model.d1()
        d2 = self.model.d2()
        S = self.model.S
        K = self.model.K
        T = self.model.T
        r = self.model.r
        sigma = self.model.sigma

        theta = (
            -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))
            - r * K * math.exp(-r * T) * norm.cdf(d2)
        )

        # Per day theta
        return theta / 365

    def put_theta(self) -> float:
        d1 = self.model.d1()
        d2 = self.model.d2()
        S = self.model.S
        K = self.model.K
        T = self.model.T
        r = self.model.r
        sigma = self.model.sigma

        theta = (
            -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))
            + r * K * math.exp(-r * T) * norm.cdf(-d2)
        )

        # Per day theta
        return theta / 365

    def call_rho(self) -> float:
        d2 = self.model.d2()
        K = self.model.K
        T = self.model.T
        r = self.model.r

        # Divided by 100 to represent change per 1 percentage point rate move
        return (K * T * math.exp(-r * T) * norm.cdf(d2)) / 100

    def put_rho(self) -> float:
        d2 = self.model.d2()
        K = self.model.K
        T = self.model.T
        r = self.model.r

        # Divided by 100 to represent change per 1 percentage point rate move
        return (-K * T * math.exp(-r * T) * norm.cdf(-d2)) / 100