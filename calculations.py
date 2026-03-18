from dataclasses import dataclass

MIN_N = 100
MAX_N = 1000
MIN_RATE = 0.001
MAX_BASE_RATE = 0.50
MIN_SENSITIVITY = 0.50
MAX_SENSITIVITY = 0.999
MAX_FPR = 0.50


@dataclass
class BayesianParameters:
    N: int
    base_rate: float
    sensitivity: float
    fpr: float


@dataclass
class DerivedCounts:
    N: int
    n_disease: int
    n_healthy: int
    true_positive: int
    false_negative: int
    false_positive: int
    true_negative: int
    total_test_positive: int
    total_test_negative: int
    posterior_ppv: float


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def compute(params: BayesianParameters) -> DerivedCounts:
    """Compute natural-frequency counts and posterior from Bayes parameters."""
    N = int(_clamp(params.N, MIN_N, MAX_N))
    base_rate = _clamp(params.base_rate, MIN_RATE, MAX_BASE_RATE)
    sensitivity = _clamp(params.sensitivity, MIN_SENSITIVITY, MAX_SENSITIVITY)
    fpr = _clamp(params.fpr, MIN_RATE, MAX_FPR)

    n_disease = round(N * base_rate)
    n_healthy = N - n_disease

    true_positive = round(n_disease * sensitivity)
    false_negative = n_disease - true_positive

    false_positive = round(n_healthy * fpr)
    true_negative = n_healthy - false_positive

    total_test_positive = true_positive + false_positive
    total_test_negative = false_negative + true_negative

    posterior_ppv = true_positive / total_test_positive if total_test_positive > 0 else 0.0

    return DerivedCounts(
        N=N,
        n_disease=n_disease,
        n_healthy=n_healthy,
        true_positive=true_positive,
        false_negative=false_negative,
        false_positive=false_positive,
        true_negative=true_negative,
        total_test_positive=total_test_positive,
        total_test_negative=total_test_negative,
        posterior_ppv=posterior_ppv,
    )
