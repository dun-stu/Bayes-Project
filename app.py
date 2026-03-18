import streamlit as st

from calculations import BayesianParameters, compute
from frequency_tree import create_frequency_tree
from icon_array import create_icon_array
from scenarios import SCENARIOS
from text_layer import generate_problem_text

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
N = st.sidebar.select_slider(
    "Population size (N)",
    options=[100, 200, 500, 1000],
    key="N",
)
base_rate_pct = st.sidebar.slider(
    "Base rate (prevalence)",
    0.1,
    50.0,
    step=0.1,
    format="%.1f%%",
    key="base_rate_pct",
)
sensitivity_pct = st.sidebar.slider(
    "Sensitivity",
    50.0,
    99.9,
    step=0.1,
    format="%.1f%%",
    key="sensitivity_pct",
)
fpr_pct = st.sidebar.slider(
    "False positive rate",
    0.1,
    50.0,
    step=0.1,
    format="%.1f%%",
    key="fpr_pct",
)

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
    st.metric(
        "Posterior (PPV)",
        f"P(Disease | Test⁺) = {counts.true_positive}/{counts.total_test_positive} ≈ {counts.posterior_ppv:.3f}",
        f"{counts.posterior_ppv * 100:.1f}%",
    )
else:
    st.metric(
        "Posterior (PPV)",
        f"{counts.true_positive} out of {counts.total_test_positive}",
        f"{counts.posterior_ppv * 100:.1f}% actually {domain['condition']}",
    )
