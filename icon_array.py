import math
from typing import List

import plotly.graph_objects as go

from calculations import DerivedCounts

COLORS = {
    "neutral": "#9CA3AF",
    "disease_group": "#F97316",
    "true_positive": "#EA580C",
    "false_negative": "#FDBA74",
    "healthy_group": "#3B82F6",
    "true_negative": "#1D4ED8",
    "false_positive": "#93C5FD",
}

MIN_MARKER_SIZE = 8
MAX_MARKER_SIZE = 26
MARKER_SIZE_BASE = 520
RIGHT_LEGEND_MARGIN = 260


def compute_grid(N: int) -> tuple[int, int]:
    """Return (rows, cols) for a near-square grid containing N cells."""
    cols = math.ceil(math.sqrt(N))
    rows = math.ceil(N / cols)
    return rows, cols


def _format_region_value(count: int, N: int, framing: str) -> str:
    if framing == "probability":
        return f"{(count / N * 100) if N else 0:.1f}%"
    return str(count)


def _region_defs(counts: DerivedCounts, domain: dict, grouping: str) -> List[dict]:
    tp_text = f"{domain['condition'].capitalize()} + {domain['test_positive']}"
    fn_text = f"{domain['condition'].capitalize()} + {domain['test_negative']}"
    fp_text = f"{domain['condition_neg'].capitalize()} + {domain['test_positive']}"
    tn_text = f"{domain['condition_neg'].capitalize()} + {domain['test_negative']}"

    if grouping == "test_result":
        return [
            {
                "key": "true_positive",
                "count": counts.true_positive,
                "color": COLORS["true_positive"],
                "domain_label": tp_text,
                "struct_label": "True Positive",
            },
            {
                "key": "false_positive",
                "count": counts.false_positive,
                "color": COLORS["false_positive"],
                "domain_label": fp_text,
                "struct_label": "False Positive",
            },
            {
                "key": "false_negative",
                "count": counts.false_negative,
                "color": COLORS["false_negative"],
                "domain_label": fn_text,
                "struct_label": "False Negative",
            },
            {
                "key": "true_negative",
                "count": counts.true_negative,
                "color": COLORS["true_negative"],
                "domain_label": tn_text,
                "struct_label": "True Negative",
            },
        ]

    return [
        {
            "key": "true_positive",
            "count": counts.true_positive,
            "color": COLORS["true_positive"],
            "domain_label": tp_text,
            "struct_label": "True Positive",
        },
        {
            "key": "false_negative",
            "count": counts.false_negative,
            "color": COLORS["false_negative"],
            "domain_label": fn_text,
            "struct_label": "False Negative",
        },
        {
            "key": "false_positive",
            "count": counts.false_positive,
            "color": COLORS["false_positive"],
            "domain_label": fp_text,
            "struct_label": "False Positive",
        },
        {
            "key": "true_negative",
            "count": counts.true_negative,
            "color": COLORS["true_negative"],
            "domain_label": tn_text,
            "struct_label": "True Negative",
        },
    ]


def _compute_marker_size(rows: int, cols: int) -> int:
    return max(MIN_MARKER_SIZE, min(MAX_MARKER_SIZE, int(MARKER_SIZE_BASE / max(rows, cols))))


def create_icon_array(
    counts: DerivedCounts,
    domain: dict,
    framing: str,
    grouping: str,
) -> go.Figure:
    """Return a Plotly figure of the icon array."""
    rows, cols = compute_grid(counts.N)
    capacity = rows * cols

    regions = _region_defs(counts, domain, grouping)
    color_by_index = []
    hover_by_index = []

    cursor = 0
    for region in regions:
        for _ in range(region["count"]):
            if cursor >= counts.N:
                break
            color_by_index.append(region["color"])
            value_label = _format_region_value(region["count"], counts.N, framing)
            hover_by_index.append(
                f"{region['domain_label']}<br>{region['struct_label']}<br>"
                f"Value: {value_label}"
            )
            cursor += 1

    while len(color_by_index) < counts.N:
        color_by_index.append(COLORS["neutral"])
        hover_by_index.append("Unassigned")

    while len(color_by_index) < capacity:
        color_by_index.append("rgba(0,0,0,0)")
        hover_by_index.append("Padding")

    xs, ys = [], []
    for idx in range(capacity):
        row = idx // cols
        col = idx % cols
        xs.append(col)
        ys.append(rows - 1 - row)

    marker_size = _compute_marker_size(rows, cols)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers",
            marker={
                "symbol": "square",
                "size": marker_size,
                "color": color_by_index,
                "line": {"width": 0},
            },
            hovertemplate="%{text}<extra></extra>",
            text=hover_by_index,
            showlegend=False,
        )
    )

    fig.update_layout(
        margin={"l": 10, "r": RIGHT_LEGEND_MARGIN, "t": 10, "b": 10},
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend={
            "orientation": "v",
            "yanchor": "top",
            "y": 1.0,
            "xanchor": "left",
            "x": 1.02,
            "font": {"size": 11},
        },
        xaxis={
            "visible": False,
            "range": [-0.6, cols - 0.4],
            "scaleanchor": "y",
            "fixedrange": True,
        },
        yaxis={"visible": False, "range": [-0.6, rows - 0.4], "fixedrange": True},
        height=max(360, min(760, int(rows * marker_size * 1.35))),
    )

    legend_traces = []
    for region in regions:
        legend_traces.append(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={"symbol": "square", "size": 11, "color": region["color"]},
                name=f"{region['struct_label']}: {region['domain_label']}",
                hoverinfo="skip",
                showlegend=True,
            )
        )
    fig.add_traces(legend_traces)

    return fig
