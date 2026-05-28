import math
from dataclasses import dataclass
from scipy.stats import norm


@dataclass
class BlackScholesModel:
    """
    Black-Scholes model for European call and put options.

    Parameters
    ----------
    S : float
        Current underlying asset price.
    K : float
        Strike price.
    T : float
        Time to maturity in years.
    r : float
        Continuously compounded risk-free rate.
    sigma : float
        Volatility of the underlying asset.
    """

    S: float
    K: float
    T: float
    r: float
    sigma: float

    def __post_init__(self):
        self.validate_inputs()

    def validate_inputs(self):
        if self.S <= 0:
            raise ValueError("Underlying price S must be positive.")
        if self.K <= 0:
            raise ValueError("Strike price K must be positive.")
        if self.T <= 0:
            raise ValueError("Time to maturity T must be positive.")
        if self.sigma <= 0:
            raise ValueError("Volatility sigma must be positive.")

    def d1(self) -> float:
        numerator = math.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T
        denominator = self.sigma * math.sqrt(self.T)
        return numerator / denominator

    def d2(self) -> float:
        return self.d1() - self.sigma * math.sqrt(self.T)

    def call_price(self) -> float:
        d1 = self.d1()
        d2 = self.d2()

        return self.S * norm.cdf(d1) - self.K * math.exp(-self.r * self.T) * norm.cdf(d2)

    def put_price(self) -> float:
        d1 = self.d1()
        d2 = self.d2()

        return self.K * math.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)