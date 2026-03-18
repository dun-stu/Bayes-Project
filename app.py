import streamlit as st

from calculations import BayesianParameters, compute
from frequency_tree import create_frequency_tree
from icon_array import create_icon_array
from scenarios import SCENARIOS
from text_layer import generate_bayes_explanation, generate_problem_text

st.set_page_config(page_title="Bayesian Reasoning Tool", page_icon="🎲", layout="wide")

DEFAULT_DOMAIN = {
    "population": "people",
    "condition": "have the condition",
    "condition_neg": "do not have the condition",
    "test": "the test",
    "test_positive": "test positive",
    "test_negative": "test negative",
}
DEFAULTS = {"N": 200, "base_rate": 0.05, "sensitivity": 0.90, "fpr": 0.05}
BASE_RATE_OPTIONS_PCT = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0]
SENSITIVITY_OPTIONS_PCT = [60.0, 70.0, 80.0, 85.0, 90.0, 95.0, 97.0, 98.0, 99.0, 99.5, 99.9]
FPR_OPTIONS_PCT = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0]


def _ensure_current_in_options(options: list[float], current: float) -> list[float]:
    rounded = round(float(current), 1)
    if rounded in options:
        return options
    return sorted(set([*options, rounded]))

if "icon_grouping" not in st.session_state:
    st.session_state.icon_grouping = False
if "probability_tree" not in st.session_state:
    st.session_state.probability_tree = False
if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = SCENARIOS[0]["name"]

# Sidebar
st.sidebar.header("Scenario")
scenario_names = [scenario["name"] for scenario in SCENARIOS] + ["Custom"]
selected = st.sidebar.selectbox(
    "Choose a scenario",
    scenario_names,
    index=scenario_names.index(st.session_state.selected_scenario)
    if st.session_state.selected_scenario in scenario_names
    else 0,
)

if selected != "Custom":
    scenario = next(s for s in SCENARIOS if s["name"] == selected)
    domain = scenario["domain"]
    defaults = scenario["defaults"]
else:
    domain = DEFAULT_DOMAIN
    defaults = DEFAULTS

if selected != st.session_state.selected_scenario:
    st.session_state.selected_scenario = selected
    st.session_state.N = defaults["N"]
    st.session_state.base_rate_pct = defaults["base_rate"] * 100
    st.session_state.sensitivity_pct = defaults["sensitivity"] * 100
    st.session_state.fpr_pct = defaults["fpr"] * 100
else:
    st.session_state.setdefault("N", defaults["N"])
    st.session_state.setdefault("base_rate_pct", defaults["base_rate"] * 100)
    st.session_state.setdefault("sensitivity_pct", defaults["sensitivity"] * 100)
    st.session_state.setdefault("fpr_pct", defaults["fpr"] * 100)

st.sidebar.header("Parameters")
if st.session_state.sensitivity_pct < 60.0:
    st.session_state.sensitivity_pct = 60.0
N = st.sidebar.select_slider(
    "Population size (N)",
    options=[100, 200, 500, 1000],
    key="N",
)
base_rate_pct = st.sidebar.select_slider(
    "Base rate (prevalence)",
    options=_ensure_current_in_options(BASE_RATE_OPTIONS_PCT, st.session_state.base_rate_pct),
    format_func=lambda value: f"{value:.1f}%",
    key="base_rate_pct",
)
sensitivity_pct = st.sidebar.select_slider(
    "Sensitivity",
    options=_ensure_current_in_options(SENSITIVITY_OPTIONS_PCT, st.session_state.sensitivity_pct),
    format_func=lambda value: f"{value:.1f}%",
    key="sensitivity_pct",
)
fpr_options = [value for value in FPR_OPTIONS_PCT if value < sensitivity_pct]
if not fpr_options:
    fpr_options = [0.1]
if st.session_state.fpr_pct not in fpr_options:
    st.session_state.fpr_pct = min(fpr_options, key=lambda value: abs(value - st.session_state.fpr_pct))
fpr_pct = st.sidebar.select_slider(
    "False positive rate",
    options=fpr_options,
    format_func=lambda value: f"{value:.1f}%",
    key="fpr_pct",
)
st.sidebar.caption("Constraint: false positive rate is kept below sensitivity.")

st.sidebar.header("Display")
framing = "probability" if st.sidebar.toggle("Show as probabilities", value=False) else "frequency"

params = BayesianParameters(
    N=N,
    base_rate=base_rate_pct / 100,
    sensitivity=sensitivity_pct / 100,
    fpr=fpr_pct / 100,
)
counts = compute(params)
problem = generate_problem_text(counts, params, domain, framing)
bayes_explanation = generate_bayes_explanation(counts, params, domain, framing)

st.title("🎲 Bayesian Reasoning Tool")
st.markdown(problem["description"])
st.info(problem["question"])

icon_tab, tree_tab = st.tabs(["Icon Array", "Frequency Tree"])

with icon_tab:
    st.toggle("Group by test result", key="icon_grouping")
    icon_fig = create_icon_array(
        counts=counts,
        domain=domain,
        framing=framing,
        grouping="test_result" if st.session_state.icon_grouping else "condition",
    )
    st.plotly_chart(icon_fig, use_container_width=True)

with tree_tab:
    st.toggle("Show as probability tree", key="probability_tree")
    tree_fig = create_frequency_tree(
        counts=counts,
        params=params,
        domain=domain,
        framing=framing,
        tree_type="probability_tree" if st.session_state.probability_tree else "frequency_tree",
    )
    st.plotly_chart(tree_fig, use_container_width=True)

st.markdown("### Posterior answer")
if counts.total_test_positive == 0:
    st.metric("Posterior (PPV)", "Undefined", "No positive test results")
elif framing == "probability":
    condition_label = domain["condition"].capitalize()
    st.metric(
        "Posterior (PPV)",
        f"P({condition_label} | Test⁺) = {counts.true_positive}/{counts.total_test_positive} ≈ {counts.posterior_ppv:.3f}",
        f"{counts.posterior_ppv * 100:.1f}%",
    )
else:
    st.metric(
        "Posterior (PPV)",
        f"{counts.true_positive} out of {counts.total_test_positive}",
        f"{counts.posterior_ppv * 100:.1f}% actually {domain['condition']}",
    )

with st.expander("Show Bayes' rule calculation + visual mapping", expanded=True):
    explanation_col, bayes_panel_col = st.columns([1, 1], gap="large")

    with explanation_col:
        st.markdown(f"**Text form**  \n{bayes_explanation['formula']}")
        st.markdown(f"**Current-value text substitution**  \n{bayes_explanation['substitution']}")
        st.markdown("**Quick visual-reading summary**")
        for line in bayes_explanation["mapping"]:
            st.markdown(f"- {line}")

    with bayes_panel_col:
        (bayes_math_tab,) = st.tabs(["Bayes rule mapping/math"])
        with bayes_math_tab:
            st.markdown("**Original Bayes' rule**")
            st.latex(bayes_explanation["latex_original"])
            st.markdown("**Expanded with total probability**")
            st.latex(bayes_explanation["latex_expanded"])
            st.markdown("**Substitute current values**")
            st.latex(bayes_explanation["latex_substitution"])
            if framing == "frequency":
                st.markdown("**Equivalent frequency form**")
                st.latex(bayes_explanation["latex_frequency_form"])
            st.markdown("**How each equation part maps to the visuals**")
            for part in bayes_explanation["term_mapping"]:
                st.latex(part["term"])
                st.markdown(f"- {part['meaning']} {part['visual']}")
