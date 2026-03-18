from typing import Dict

import plotly.graph_objects as go

from calculations import BayesianParameters, DerivedCounts
from icon_array import COLORS

POSTERIOR_BRACKET_Y = 0.14
POSTERIOR_BRACKET_TICK_Y = 0.11


def _as_pct(value: float, digits: int = 1) -> str:
    return f"{value * 100:.{digits}f}%"


def _as_prob(value: float) -> str:
    return f"{value:.3g}" if value else "0"


def _node_value(count: int, total: int, use_probability: bool) -> str:
    if use_probability:
        return _as_prob(count / total if total else 0.0)
    return str(count)


def _add_node(
    fig: go.Figure,
    x: float,
    y: float,
    color: str,
    domain_label: str,
    struct_label: str,
    value_text: str,
    width: float = 0.18,
    height: float = 0.12,
) -> None:
    fig.add_shape(
        type="rect",
        x0=x - width / 2,
        x1=x + width / 2,
        y0=y - height / 2,
        y1=y + height / 2,
        line={"color": color, "width": 2},
        fillcolor=color,
        opacity=0.92,
    )
    fig.add_annotation(
        x=x,
        y=y,
        showarrow=False,
        text=(
            f"<span style='font-size:10px'>{domain_label}</span><br>"
            f"<b style='font-size:20px'>{value_text}</b><br>"
            f"<span style='font-size:10px;color:#E5E7EB'>({struct_label})</span>"
        ),
        font={"color": "white"},
        align="center",
    )


def create_frequency_tree(
    counts: DerivedCounts,
    params: BayesianParameters,
    domain: dict,
    framing: str,
    tree_type: str,
) -> go.Figure:
    """Return a Plotly figure of the frequency/probability tree."""
    use_probability = framing == "probability" or tree_type == "probability_tree"

    positions: Dict[str, tuple[float, float]] = {
        "root": (0.50, 1.00),
        "disease": (0.30, 0.66),
        "healthy": (0.70, 0.66),
        "tp": (0.14, 0.32),
        "fn": (0.38, 0.32),
        "fp": (0.62, 0.32),
        "tn": (0.86, 0.32),
    }

    fig = go.Figure()

    for src, dst in [
        ("root", "disease"),
        ("root", "healthy"),
        ("disease", "tp"),
        ("disease", "fn"),
        ("healthy", "fp"),
        ("healthy", "tn"),
    ]:
        x0, y0 = positions[src]
        x1, y1 = positions[dst]
        fig.add_shape(type="line", x0=x0, y0=y0 - 0.07, x1=x1, y1=y1 + 0.07, line={"color": "#6B7280", "width": 2})

    if use_probability:
        branch_labels = [
            ((0.40, 0.83), f"P(D) = {_as_prob(params.base_rate)}"),
            ((0.60, 0.83), f"P(¬D) = {_as_prob(1 - params.base_rate)}"),
            ((0.22, 0.49), f"P(T⁺|D) = {_as_prob(params.sensitivity)}"),
            ((0.34, 0.49), f"P(T⁻|D) = {_as_prob(1 - params.sensitivity)}"),
            ((0.66, 0.49), f"P(T⁺|¬D) = {_as_prob(params.fpr)}"),
            ((0.78, 0.49), f"P(T⁻|¬D) = {_as_prob(1 - params.fpr)}"),
        ]
    else:
        branch_labels = [
            ((0.40, 0.83), f"Prevalence: {_as_pct(params.base_rate)}"),
            ((0.60, 0.83), f"No condition: {_as_pct(1 - params.base_rate)}"),
            ((0.22, 0.49), f"Sensitivity: {_as_pct(params.sensitivity)}"),
            ((0.34, 0.49), f"Miss rate: {_as_pct(1 - params.sensitivity)}"),
            ((0.66, 0.49), f"FPR: {_as_pct(params.fpr)}"),
            ((0.78, 0.49), f"Specificity: {_as_pct(1 - params.fpr)}"),
        ]

    for (x, y), label in branch_labels:
        fig.add_annotation(x=x, y=y, text=label, showarrow=False, font={"size": 11, "color": "#374151"})

    _add_node(
        fig,
        *positions["root"],
        COLORS["neutral"],
        f"{domain['population'].capitalize()}",
        "Population",
        _node_value(counts.N, counts.N, use_probability),
    )
    _add_node(
        fig,
        *positions["disease"],
        COLORS["disease_group"],
        domain["condition"].capitalize(),
        "Condition-positive",
        _node_value(counts.n_disease, counts.N, use_probability),
    )
    _add_node(
        fig,
        *positions["healthy"],
        COLORS["healthy_group"],
        domain["condition_neg"].capitalize(),
        "Condition-negative",
        _node_value(counts.n_healthy, counts.N, use_probability),
    )

    _add_node(
        fig,
        *positions["tp"],
        COLORS["true_positive"],
        domain["test_positive"].capitalize(),
        "True Positive",
        _node_value(counts.true_positive, counts.N, use_probability),
        width=0.16,
    )
    _add_node(
        fig,
        *positions["fn"],
        COLORS["false_negative"],
        domain["test_negative"].capitalize(),
        "False Negative",
        _node_value(counts.false_negative, counts.N, use_probability),
        width=0.16,
    )
    _add_node(
        fig,
        *positions["fp"],
        COLORS["false_positive"],
        domain["test_positive"].capitalize(),
        "False Positive",
        _node_value(counts.false_positive, counts.N, use_probability),
        width=0.16,
    )
    _add_node(
        fig,
        *positions["tn"],
        COLORS["true_negative"],
        domain["test_negative"].capitalize(),
        "True Negative",
        _node_value(counts.true_negative, counts.N, use_probability),
        width=0.16,
    )

    fig.add_shape(
        type="line",
        x0=positions["tp"][0],
        y0=POSTERIOR_BRACKET_Y,
        x1=positions["fp"][0],
        y1=POSTERIOR_BRACKET_Y,
        line={"color": "#111827", "width": 3},
    )
    fig.add_shape(
        type="line",
        x0=positions["tp"][0],
        y0=POSTERIOR_BRACKET_Y,
        x1=positions["tp"][0],
        y1=POSTERIOR_BRACKET_TICK_Y,
        line={"color": "#111827", "width": 3},
    )
    fig.add_shape(
        type="line",
        x0=positions["fp"][0],
        y0=POSTERIOR_BRACKET_Y,
        x1=positions["fp"][0],
        y1=POSTERIOR_BRACKET_TICK_Y,
        line={"color": "#111827", "width": 3},
    )

    if counts.total_test_positive == 0:
        posterior_text = "PPV is undefined (no positive test results)"
    elif use_probability:
        posterior_text = (
            f"P(D|T⁺) = {counts.true_positive}/{counts.total_test_positive} "
            f"≈ {_as_prob(counts.posterior_ppv)}"
        )
    else:
        posterior_text = (
            f"PPV: {counts.true_positive} out of {counts.total_test_positive} "
            f"= {_as_pct(counts.posterior_ppv)}"
        )

    combo_text = (
        f"Test positive: {counts.true_positive} + {counts.false_positive} "
        f"= {counts.total_test_positive}<br>{posterior_text}"
    )
    fig.add_annotation(
        x=0.50,
        y=0.07,
        text=combo_text,
        showarrow=False,
        font={"size": 13, "color": "#111827"},
        align="center",
    )

    fig.update_layout(
        xaxis={"visible": False, "range": [0.02, 0.98], "fixedrange": True},
        yaxis={"visible": False, "range": [0.0, 1.08], "fixedrange": True},
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=700,
    )

    return fig
