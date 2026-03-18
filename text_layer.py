from calculations import BayesianParameters, DerivedCounts


def _pct(value: float, digits: int = 1) -> str:
    return f"{value * 100:.{digits}f}%"


def generate_problem_text(
    counts: DerivedCounts,
    params: BayesianParameters,
    domain: dict,
    framing: str,
) -> dict:
    """Return scenario description and question in selected framing."""
    if framing == "probability":
        description = (
            f"The prevalence of the condition is **{_pct(params.base_rate)}**. "
            f"{domain['test'].capitalize()} has a sensitivity of **{_pct(params.sensitivity)}** "
            f"and a false positive rate of **{_pct(params.fpr)}**."
        )
        question = (
            "What is the probability that someone who tests positive actually has the condition? "
            "What is P(Condition | Test⁺)?"
        )
        return {"description": description, "question": question}

    description = (
        f"Imagine **{counts.N} {domain['population']}**. "
        f"Of these {counts.N}, **{counts.n_disease} {domain['condition']}**. "
        f"Of the {counts.n_disease} who {domain['condition']}, "
        f"**{counts.true_positive} {domain['test_positive']}**. "
        f"Of the {counts.n_healthy} who {domain['condition_neg']}, "
        f"**{counts.false_positive} {domain['test_positive']}**."
    )
    question = f"Of all those who {domain['test_positive']}, how many actually {domain['condition']}?"
    return {"description": description, "question": question}
