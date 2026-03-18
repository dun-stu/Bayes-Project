from calculations import BayesianParameters, DerivedCounts

LATEX_BAYES_ORIGINAL = r"P(D \mid T^+) = \frac{P(T^+ \mid D)\,P(D)}{P(T^+)}"
LATEX_BAYES_EXPANDED = (
    r"P(D \mid T^+) = "
    r"\frac{P(T^+ \mid D)\,P(D)}{P(T^+ \mid D)\,P(D) + P(T^+ \mid \neg D)\,P(\neg D)}"
)


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


def generate_bayes_explanation(
    counts: DerivedCounts,
    params: BayesianParameters,
    domain: dict,
    framing: str,
) -> dict:
    """Return Bayes-rule explanation text and visual mapping in selected framing."""
    condition_label = domain["condition"].capitalize()
    condition_neg_label = domain["condition_neg"].capitalize()
    test_pos_label = domain["test_positive"]

    if framing == "probability":
        formula = (
            "P(Condition | Test⁺) = "
            "[P(Test⁺ | Condition) × P(Condition)] / "
            "[P(Test⁺ | Condition) × P(Condition) + P(Test⁺ | ¬Condition) × P(¬Condition)]"
        )
        substitution = (
            f"P({condition_label} | Test⁺) = "
            f"({params.sensitivity:.3f} × {params.base_rate:.3f}) / "
            f"(({params.sensitivity:.3f} × {params.base_rate:.3f}) + "
            f"({params.fpr:.3f} × {1 - params.base_rate:.3f})) = {counts.posterior_ppv:.3f}"
        )
    else:
        formula = "Posterior (PPV) = True Positives / (True Positives + False Positives)"
        substitution = (
            f"PPV = {counts.true_positive} / ({counts.true_positive} + {counts.false_positive}) "
            f"= {counts.true_positive}/{counts.total_test_positive} = {counts.posterior_ppv:.3f}"
        )

    tp_path_prob = f"{params.sensitivity:.3f}\\times{params.base_rate:.3f}"
    fp_path_prob = f"{params.fpr:.3f}\\times{1 - params.base_rate:.3f}"
    latex_substitution = (
        r"P(D \mid T^+) = "
        r"\frac{"
        f"{tp_path_prob}"
        r"}{"
        f"{tp_path_prob}"
        r" + "
        f"{fp_path_prob}"
        r"}"
        f" = {counts.posterior_ppv:.3f}"
    )
    latex_frequency_form = (
        r"P(D \mid T^+) = "
        r"\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}}"
        r" = "
        rf"\frac{{{counts.true_positive}}}{{{counts.true_positive}+{counts.false_positive}}}"
        f" = {counts.posterior_ppv:.3f}"
    )

    mapping = [
        (
            f"Icon Array: numerator is the **True Positive** region "
            f"({condition_label} ∩ {test_pos_label}) = **{counts.true_positive}**."
        ),
        (
            f"Icon Array: denominator is everyone who {test_pos_label}: "
            f"**True Positive ({counts.true_positive}) + False Positive ({counts.false_positive}) "
            f"= {counts.total_test_positive}**."
        ),
        (
            "Frequency Tree: numerator follows the branch "
            f"**{condition_label} → {test_pos_label}**."
        ),
        (
            "Frequency Tree: denominator combines both positive-test branches: "
            f"**{condition_label} → {test_pos_label}** and "
            f"**{condition_neg_label} → {test_pos_label}**."
        ),
    ]
    term_mapping = [
        {
            "term": r"P(T^+ \mid D)\,P(D)",
            "meaning": "True-positive pathway contribution.",
            "visual": (
                f"Tree branch {condition_label} → {test_pos_label}; "
                f"icon-array True Positive region ({counts.true_positive})."
            ),
        },
        {
            "term": r"P(T^+ \mid \neg D)\,P(\neg D)",
            "meaning": "False-positive pathway contribution.",
            "visual": (
                f"Tree branch {condition_neg_label} → {test_pos_label}; "
                f"icon-array False Positive region ({counts.false_positive})."
            ),
        },
        {
            "term": r"P(T^+)",
            "meaning": "All positive tests in the denominator.",
            "visual": f"True Positive + False Positive = {counts.total_test_positive}.",
        },
    ]
    return {
        "formula": formula,
        "substitution": substitution,
        "mapping": mapping,
        "latex_original": LATEX_BAYES_ORIGINAL,
        "latex_expanded": LATEX_BAYES_EXPANDED,
        "latex_substitution": latex_substitution,
        "latex_frequency_form": latex_frequency_form,
        "term_mapping": term_mapping,
    }
