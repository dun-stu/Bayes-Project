import math
from typing import Dict, List

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
LOW_N_THRESHOLD = 200
MID_N_THRESHOLD = 500
LOW_ANNOTATION_FONT = 11
MID_ANNOTATION_FONT = 13
HIGH_ANNOTATION_FONT = 15
EXTERNAL_LABEL_RATIO_THRESHOLD = 0.12
EXTERNAL_LABEL_X_OFFSET = 2.2
EXTERNAL_LABEL_X_PIXELS_PER_GRID_UNIT = 72
EXTERNAL_LABEL_BASE_X_PIXELS = 120
EXTERNAL_LABEL_BASE_Y_PIXELS = -36
EXTERNAL_LABEL_Y_SPACING_PIXELS = 30
EXTERNAL_LABEL_X_RANGE_EXPANSION = 4.2


def compute_grid(N: int) -> tuple[int, int]:
    """Return (rows, cols) for a near-square grid containing N cells."""
    cols = math.ceil(math.sqrt(N))
    rows = math.ceil(N / cols)
    return rows, cols


def _format_region_value(count: int, N: int, framing: str) -> str:
    if framing == "probability":
        return f"{(count / N * 100) if N else 0:.1f}%"
    return str(count)


def _region_defs(counts: DerivedCounts, domain: dict, grouping: str) -> List[Dict]:
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


def _annotation_font_size(N: int) -> int:
    if N <= LOW_N_THRESHOLD:
        return LOW_ANNOTATION_FONT
    if N < MID_N_THRESHOLD:
        return MID_ANNOTATION_FONT
    return HIGH_ANNOTATION_FONT


def _compute_marker_size(rows: int, cols: int) -> int:
    return max(MIN_MARKER_SIZE, min(MAX_MARKER_SIZE, int(MARKER_SIZE_BASE / max(rows, cols))))


def _format_domain_label(domain_label: str) -> str:
    return domain_label.replace(" + ", "<br>")


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
    region_indices: Dict[str, List[int]] = {region["key"]: [] for region in regions}

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
            region_indices[region["key"]].append(cursor)
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

    annotation_font = _annotation_font_size(counts.N)
    external_label_slots = 0
    has_external_labels = False
    for region in regions:
        region_idx = region_indices.get(region["key"], [])
        if not region_idx:
            continue
        centroid_x = sum((idx % cols) for idx in region_idx) / len(region_idx)
        centroid_y = sum((rows - 1 - (idx // cols)) for idx in region_idx) / len(region_idx)
        value_text = _format_region_value(region["count"], counts.N, framing)
        label_text = (
            f"<b>{_format_domain_label(region['domain_label'])}</b><br>"
            f"{value_text}<br>"
            f"<span style='color:#6B7280;font-size:{max(annotation_font - 2, 9)}px'>"
            f"({region['struct_label']})"
            "</span>"
        )
        use_external_label = (region["count"] / counts.N) < EXTERNAL_LABEL_RATIO_THRESHOLD

        if use_external_label:
            has_external_labels = True
            external_label_slots += 1
            fig.add_annotation(
                x=centroid_x,
                y=centroid_y,
                text=label_text,
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowcolor="#6B7280",
                ax=int((EXTERNAL_LABEL_X_OFFSET * EXTERNAL_LABEL_X_PIXELS_PER_GRID_UNIT) + EXTERNAL_LABEL_BASE_X_PIXELS),
                ay=int(EXTERNAL_LABEL_BASE_Y_PIXELS - ((external_label_slots - 1) * EXTERNAL_LABEL_Y_SPACING_PIXELS)),
                align="left",
                font={"size": max(annotation_font - 1, 10), "color": "#111827"},
                bgcolor="rgba(255,255,255,0.92)",
                borderpad=3,
            )
        else:
            fig.add_annotation(
                x=centroid_x,
                y=centroid_y,
                text=label_text,
                showarrow=False,
                align="center",
                font={"size": annotation_font, "color": "#111827"},
                bgcolor="rgba(255,255,255,0.78)",
                borderpad=2,
            )

    fig.update_layout(
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis={
            "visible": False,
            "range": [-0.6, cols + (EXTERNAL_LABEL_X_RANGE_EXPANSION if has_external_labels else -0.4)],
            "scaleanchor": "y",
        },
        yaxis={"visible": False, "range": [-0.6, rows - 0.4]},
        height=max(360, min(760, int(rows * marker_size * 1.35))),
    )

    return fig
