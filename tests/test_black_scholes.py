import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.black_scholes import BlackScholesModel
from src.validation import put_call_parity_check


def test_black_scholes_benchmark_prices():
    model = BlackScholesModel(S=100, K=100, T=1, r=0.05, sigma=0.20)

    assert round(model.call_price(), 4) == 10.4506
    assert round(model.put_price(), 4) == 5.5735


def test_put_call_parity_error_is_near_zero():
    model = BlackScholesModel(S=100, K=100, T=1, r=0.05, sigma=0.20)
    parity = put_call_parity_check(model)

    assert abs(parity["parity_error"]) < 1e-8
    assert parity["parity_pass"]


def test_invalid_inputs_raise_error():
    try:
        BlackScholesModel(S=-100, K=100, T=1, r=0.05, sigma=0.20)
        assert False
    except ValueError:
        assert True