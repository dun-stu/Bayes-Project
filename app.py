"""
Probability Visualization App
A Streamlit application to visualize probability concepts using grids and colors.
Perfect for teaching Bayes' rule and other probability concepts with whole numbers.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgba
from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Scenario:
    """Represents a pre-built Bayes scenario with 4 mutually exclusive categories."""
    name: str
    description: str
    total: int
    grid_rows: Optional[int] = None
    grid_cols: Optional[int] = None
    # Four categories: TP, FP, FN, TN
    categories: List[Dict[str, any]] = None
    
    def __post_init__(self):
        """Calculate grid dimensions if not provided."""
        if self.grid_rows is None or self.grid_cols is None:
            # Create a near-square grid
            sqrt_total = int(np.sqrt(self.total))
            # Find factors close to square root
            for rows in range(sqrt_total, 0, -1):
                if self.total % rows == 0:
                    self.grid_rows = rows
                    self.grid_cols = self.total // rows
                    break


def get_built_in_scenarios() -> List[Scenario]:
    """Return a list of built-in teaching scenarios."""
    scenarios = []
    
    # Scenario 1: Rare disease with imperfect test (classic Bayes example)
    scenarios.append(Scenario(
        name="Rare Disease Test",
        description="A classic Bayes' theorem example: testing for a rare disease with a 90% accurate test.",
        total=1000,
        grid_rows=25,
        grid_cols=40,
        categories=[
            {'label': 'Has Disease & Test+', 'count': 9, 'color': '#FF6B6B'},     # TP
            {'label': 'No Disease & Test+', 'count': 99, 'color': '#FFA07A'},     # FP
            {'label': 'Has Disease & Test-', 'count': 1, 'color': '#FFD93D'},     # FN
            {'label': 'No Disease & Test-', 'count': 891, 'color': '#98D8C8'},    # TN
        ]
    ))
    
    # Scenario 2: Spam filter
    scenarios.append(Scenario(
        name="Spam Filter",
        description="Email classification: spam/not-spam vs. filter marks spam/not-spam.",
        total=1000,
        grid_rows=25,
        grid_cols=40,
        categories=[
            {'label': 'Is Spam & Marked Spam', 'count': 285, 'color': '#FF6B6B'},      # TP
            {'label': 'Not Spam & Marked Spam', 'count': 15, 'color': '#FFA07A'},      # FP
            {'label': 'Is Spam & Not Marked', 'count': 15, 'color': '#FFD93D'},        # FN
            {'label': 'Not Spam & Not Marked', 'count': 685, 'color': '#98D8C8'},      # TN
        ]
    ))
    
    # Scenario 3: Airport security screening
    scenarios.append(Scenario(
        name="Security Screening",
        description="Airport security: threat detection with imperfect screening technology.",
        total=10000,
        grid_rows=100,
        grid_cols=100,
        categories=[
            {'label': 'Threat & Detected', 'count': 45, 'color': '#FF6B6B'},          # TP
            {'label': 'No Threat & Detected', 'count': 500, 'color': '#FFA07A'},      # FP
            {'label': 'Threat & Not Detected', 'count': 5, 'color': '#FFD93D'},       # FN
            {'label': 'No Threat & Not Detected', 'count': 9450, 'color': '#98D8C8'}, # TN
        ]
    ))
    
    # Scenario 4: Drug test screening
    scenarios.append(Scenario(
        name="Drug Test",
        description="Workplace drug testing: actual drug use vs. positive/negative test results.",
        total=500,
        grid_rows=20,
        grid_cols=25,
        categories=[
            {'label': 'Uses Drugs & Test+', 'count': 38, 'color': '#FF6B6B'},     # TP
            {'label': 'No Drugs & Test+', 'count': 12, 'color': '#FFA07A'},       # FP
            {'label': 'Uses Drugs & Test-', 'count': 2, 'color': '#FFD93D'},      # FN
            {'label': 'No Drugs & Test-', 'count': 448, 'color': '#98D8C8'},      # TN
        ]
    ))
    
    return scenarios


def calculate_bayes_quantities(categories: List[Dict[str, any]]) -> Dict[str, any]:
    """
    Calculate Bayes quantities from the four categories (TP, FP, FN, TN).
    
    Args:
        categories: List of 4 categories in order [TP, FP, FN, TN]
    
    Returns:
        Dictionary with priors, likelihoods, and posteriors
    """
    if len(categories) != 4:
        return None
    
    TP = categories[0]['count']  # Has Disease & Test+
    FP = categories[1]['count']  # No Disease & Test+
    FN = categories[2]['count']  # Has Disease & Test-
    TN = categories[3]['count']  # No Disease & Test-
    
    total = TP + FP + FN + TN
    
    # Disease counts
    has_condition = TP + FN
    no_condition = FP + TN
    
    # Test positive counts
    test_positive = TP + FP
    test_negative = FN + TN
    
    # Priors
    prior_condition = has_condition / total if total > 0 else 0
    prior_no_condition = no_condition / total if total > 0 else 0
    
    # Likelihoods
    likelihood_pos_given_condition = TP / has_condition if has_condition > 0 else 0
    likelihood_pos_given_no_condition = FP / no_condition if no_condition > 0 else 0
    likelihood_neg_given_condition = FN / has_condition if has_condition > 0 else 0
    likelihood_neg_given_no_condition = TN / no_condition if no_condition > 0 else 0
    
    # Posteriors
    posterior_condition_given_pos = TP / test_positive if test_positive > 0 else 0
    posterior_no_condition_given_pos = FP / test_positive if test_positive > 0 else 0
    posterior_condition_given_neg = FN / test_negative if test_negative > 0 else 0
    posterior_no_condition_given_neg = TN / test_negative if test_negative > 0 else 0
    
    return {
        'total': total,
        'has_condition': has_condition,
        'no_condition': no_condition,
        'test_positive': test_positive,
        'test_negative': test_negative,
        'prior_condition': prior_condition,
        'prior_no_condition': prior_no_condition,
        'likelihood_pos_given_condition': likelihood_pos_given_condition,
        'likelihood_pos_given_no_condition': likelihood_pos_given_no_condition,
        'likelihood_neg_given_condition': likelihood_neg_given_condition,
        'likelihood_neg_given_no_condition': likelihood_neg_given_no_condition,
        'posterior_condition_given_pos': posterior_condition_given_pos,
        'posterior_no_condition_given_pos': posterior_no_condition_given_pos,
        'posterior_condition_given_neg': posterior_condition_given_neg,
        'posterior_no_condition_given_neg': posterior_no_condition_given_neg,
        'TP': TP,
        'FP': FP,
        'FN': FN,
        'TN': TN,
    }


# Set page configuration
st.set_page_config(
    page_title="Probability Visualizer",
    page_icon="🎲",
    layout="wide"
)

# Title and description
st.title("🎲 Probability Visualization Tool")
st.markdown("""
This tool helps visualize probability concepts using grids and colors.
Perfect for teaching Bayes' rule and other probability concepts with whole numbers instead of abstract percentages.
""")

# Sidebar for inputs
st.sidebar.header("Configuration")

# Scenario selector
built_in_scenarios = get_built_in_scenarios()
scenario_options = ["Custom (manual)"] + [s.name for s in built_in_scenarios]
selected_scenario_name = st.sidebar.selectbox(
    "Scenario",
    scenario_options,
    help="Choose a pre-built scenario or create your own custom configuration"
)

# Determine if we're in scenario mode
is_scenario_mode = selected_scenario_name != "Custom (manual)"
selected_scenario = None
if is_scenario_mode:
    selected_scenario = next(s for s in built_in_scenarios if s.name == selected_scenario_name)

# Show scenario description if in scenario mode
if is_scenario_mode and selected_scenario:
    st.sidebar.info(f"**{selected_scenario.name}**: {selected_scenario.description}")

st.sidebar.markdown("---")

# Input 1: Total whole number
if is_scenario_mode:
    total_number = selected_scenario.total
    st.sidebar.number_input(
        "Total Number of Items",
        value=total_number,
        disabled=True,
        help="Total number set by the selected scenario"
    )
else:
    total_number = st.sidebar.number_input(
        "Total Number of Items",
        min_value=1,
        max_value=10000,
        value=400,
        step=1,
        help="Total number of items to visualize (e.g., 400)"
    )

# Input 2: Grid layout
st.sidebar.subheader("Grid Layout")
col1, col2 = st.sidebar.columns(2)
with col1:
    if is_scenario_mode:
        grid_rows = selected_scenario.grid_rows
        st.number_input(
            "Rows",
            value=grid_rows,
            disabled=True
        )
    else:
        grid_rows = st.number_input(
            "Rows",
            min_value=1,
            max_value=100,
            value=20,
            step=1
        )
with col2:
    if is_scenario_mode:
        grid_cols = selected_scenario.grid_cols
        st.number_input(
            "Columns",
            value=grid_cols,
            disabled=True
        )
    else:
        grid_cols = st.number_input(
            "Columns",
            min_value=1,
            max_value=100,
            value=20,
            step=1
        )

# Verify grid matches total
grid_total = grid_rows * grid_cols
if grid_total != total_number:
    st.sidebar.warning(f"⚠️ Grid size ({grid_rows}×{grid_cols}={grid_total}) doesn't match total ({total_number})")
    st.sidebar.info(f"Suggested: {int(np.sqrt(total_number))}×{int(np.sqrt(total_number))} = {int(np.sqrt(total_number))**2}")

# Input 3: Proportions and labels
st.sidebar.subheader("Categories")

if is_scenario_mode:
    # In scenario mode, use predefined categories
    num_categories = 4
    st.sidebar.text(f"Number of Categories: {num_categories} (fixed for scenarios)")
    categories = selected_scenario.categories.copy()
else:
    # Manual mode - allow full customization
    num_categories = st.sidebar.number_input(
        "Number of Categories",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        help="How many different categories to visualize"
    )
    
    # Default colors
    default_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                      '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']
    
    categories = []
    total_proportion = 0
    
    for i in range(num_categories):
        st.sidebar.markdown(f"**Category {i+1}**")
        col1, col2, col3 = st.sidebar.columns([2, 1, 1])
        
        with col1:
            label = st.text_input(
                f"Label {i+1}",
                value=f"Category {i+1}",
                key=f"label_{i}",
                label_visibility="collapsed"
            )
        
        with col2:
            count = st.number_input(
                f"Count {i+1}",
                min_value=0,
                max_value=total_number,
                value=min(total_number // num_categories, total_number - total_proportion),
                step=1,
                key=f"count_{i}",
                label_visibility="collapsed"
            )
        
        with col3:
            color = st.color_picker(
                f"Color {i+1}",
                value=default_colors[i % len(default_colors)],
                key=f"color_{i}",
                label_visibility="collapsed"
            )
        
        categories.append({
            'label': label,
            'count': count,
            'color': color
        })
        total_proportion += count

# Display categories in scenario mode
if is_scenario_mode:
    for i, cat in enumerate(categories):
        st.sidebar.markdown(f"**{cat['label']}**: {cat['count']} ")
        st.sidebar.markdown(f"<div style='background-color: {cat['color']}; height: 20px; width: 100%; border-radius: 3px;'></div>", unsafe_allow_html=True)

# Calculate total proportion for validation
total_proportion = sum(cat['count'] for cat in categories)

# Check if proportions add up
remaining = total_number - total_proportion
if remaining != 0:
    st.sidebar.warning(f"⚠️ Total counts ({total_proportion}) differ from total number ({total_number}). Remaining: {remaining}")

# Visualization options
st.sidebar.subheader("Display Options")
shape_type = st.sidebar.selectbox(
    "Cell Shape",
    ["Square", "Circle"],
    help="Shape to use for each cell in the grid"
)

show_grid_lines = st.sidebar.checkbox("Show Grid Lines", value=True)
show_legend = st.sidebar.checkbox("Show Legend", value=True)
show_statistics = st.sidebar.checkbox("Show Statistics", value=True)

# Main content area
if st.sidebar.button("Generate Visualization", type="primary"):
    # Create the grid data
    grid_data = np.zeros(grid_total, dtype=int)
    
    # Fill grid with category indices
    start_idx = 0
    for i, category in enumerate(categories):
        end_idx = min(start_idx + category['count'], grid_total)
        grid_data[start_idx:end_idx] = i
        start_idx = end_idx
    
    # Shuffle for random distribution (optional)
    shuffle_option = st.sidebar.checkbox("Shuffle Distribution", value=False)
    if shuffle_option:
        np.random.shuffle(grid_data)
    
    # Reshape into grid
    if grid_total > total_number:
        grid_data = np.pad(grid_data, (0, grid_total - total_number), constant_values=-1)
    grid_data = grid_data[:grid_total].reshape(grid_rows, grid_cols)
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(12, 12 * grid_rows / grid_cols))
    ax.set_xlim(0, grid_cols)
    ax.set_ylim(0, grid_rows)
    ax.set_aspect('equal')
    
    # Draw cells
    cell_size = 0.9 if show_grid_lines else 1.0
    
    for row in range(grid_rows):
        for col in range(grid_cols):
            category_idx = grid_data[row, col]
            
            if category_idx >= 0 and category_idx < len(categories):
                color = categories[category_idx]['color']
            else:
                color = '#FFFFFF'  # White for empty cells
            
            if shape_type == "Square":
                rect = patches.Rectangle(
                    (col + (1 - cell_size) / 2, grid_rows - row - 1 + (1 - cell_size) / 2),
                    cell_size,
                    cell_size,
                    linewidth=0.5 if show_grid_lines else 0,
                    edgecolor='gray' if show_grid_lines else 'none',
                    facecolor=color
                )
                ax.add_patch(rect)
            else:  # Circle
                circle = patches.Circle(
                    (col + 0.5, grid_rows - row - 0.5),
                    cell_size / 2,
                    linewidth=0.5 if show_grid_lines else 0,
                    edgecolor='gray' if show_grid_lines else 'none',
                    facecolor=color
                )
                ax.add_patch(circle)
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add legend
    if show_legend:
        legend_elements = []
        for category in categories:
            legend_elements.append(
                patches.Patch(
                    facecolor=category['color'],
                    label=f"{category['label']}: {category['count']}"
                )
            )
        ax.legend(
            handles=legend_elements,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            fontsize=10
        )
    
    plt.tight_layout()
    
    # Display the plot
    st.pyplot(fig)
    
    # Show statistics
    if show_statistics:
        st.subheader("📊 Statistics")
        
        cols = st.columns(len(categories))
        for i, category in enumerate(categories):
            with cols[i]:
                percentage = (category['count'] / total_number * 100) if total_number > 0 else 0
                st.metric(
                    label=category['label'],
                    value=f"{category['count']}",
                    delta=f"{percentage:.1f}%"
                )
        
        # Additional statistics
        st.markdown("---")
        st.markdown("### Detailed Breakdown")
        
        data_rows = []
        for category in categories:
            percentage = (category['count'] / total_number * 100) if total_number > 0 else 0
            odds = f"1:{total_number/category['count']:.1f}" if category['count'] > 0 else "N/A"
            data_rows.append({
                'Category': category['label'],
                'Count': category['count'],
                'Percentage': f"{percentage:.2f}%",
                'Odds': odds,
                'Color': category['color']
            })
        
        st.dataframe(data_rows, use_container_width=True)
    
    # Show Bayes calculations for scenario mode
    if is_scenario_mode and len(categories) == 4:
        st.markdown("---")
        st.subheader("🎓 Bayes' Theorem Calculations")
        
        bayes_calc = calculate_bayes_quantities(categories)
        
        if bayes_calc:
            # Get category colors for display
            tp_color = categories[0]['color']
            fp_color = categories[1]['color']
            fn_color = categories[2]['color']
            tn_color = categories[3]['color']
            
            st.markdown("### Prior Probabilities")
            st.markdown("*The probability before seeing test results*")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**P(Condition)** = {bayes_calc['has_condition']} / {bayes_calc['total']} ≈ **{bayes_calc['prior_condition']:.4f}** ({bayes_calc['prior_condition']*100:.2f}%)")
                st.caption(f"Count: {bayes_calc['TP']} ({categories[0]['label']}) + {bayes_calc['FN']} ({categories[2]['label']})")
            with col2:
                st.markdown(f"**P(No Condition)** = {bayes_calc['no_condition']} / {bayes_calc['total']} ≈ **{bayes_calc['prior_no_condition']:.4f}** ({bayes_calc['prior_no_condition']*100:.2f}%)")
                st.caption(f"Count: {bayes_calc['FP']} ({categories[1]['label']}) + {bayes_calc['TN']} ({categories[3]['label']})")
            
            st.markdown("---")
            st.markdown("### Likelihoods")
            st.markdown("*The probability of test results given the true condition*")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**P(Test+ | Condition)**")
                st.markdown(f"{bayes_calc['TP']} / {bayes_calc['has_condition']} ≈ **{bayes_calc['likelihood_pos_given_condition']:.4f}** ({bayes_calc['likelihood_pos_given_condition']*100:.2f}%)")
                st.caption(f"Numerator: <span style='color:{tp_color}'>■</span> {categories[0]['label']}", unsafe_allow_html=True)
                
                st.markdown("**P(Test- | Condition)**")
                st.markdown(f"{bayes_calc['FN']} / {bayes_calc['has_condition']} ≈ **{bayes_calc['likelihood_neg_given_condition']:.4f}** ({bayes_calc['likelihood_neg_given_condition']*100:.2f}%)")
                st.caption(f"Numerator: <span style='color:{fn_color}'>■</span> {categories[2]['label']}", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**P(Test+ | No Condition)**")
                st.markdown(f"{bayes_calc['FP']} / {bayes_calc['no_condition']} ≈ **{bayes_calc['likelihood_pos_given_no_condition']:.4f}** ({bayes_calc['likelihood_pos_given_no_condition']*100:.2f}%)")
                st.caption(f"Numerator: <span style='color:{fp_color}'>■</span> {categories[1]['label']}", unsafe_allow_html=True)
                
                st.markdown("**P(Test- | No Condition)**")
                st.markdown(f"{bayes_calc['TN']} / {bayes_calc['no_condition']} ≈ **{bayes_calc['likelihood_neg_given_no_condition']:.4f}** ({bayes_calc['likelihood_neg_given_no_condition']*100:.2f}%)")
                st.caption(f"Numerator: <span style='color:{tn_color}'>■</span> {categories[3]['label']}", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Posteriors (Bayes' Rule)")
            st.markdown("*The probability of the condition given test results*")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**P(Condition | Test+)**")
                st.markdown(f"{bayes_calc['TP']} / {bayes_calc['test_positive']} ≈ **{bayes_calc['posterior_condition_given_pos']:.4f}** ({bayes_calc['posterior_condition_given_pos']*100:.2f}%)")
                st.caption(f"Numerator: <span style='color:{tp_color}'>■</span> {categories[0]['label']}", unsafe_allow_html=True)
                st.caption(f"Denominator: All Test+ cases ({bayes_calc['test_positive']} total)")
                
            with col2:
                st.markdown("**P(No Condition | Test+)**")
                st.markdown(f"{bayes_calc['FP']} / {bayes_calc['test_positive']} ≈ **{bayes_calc['posterior_no_condition_given_pos']:.4f}** ({bayes_calc['posterior_no_condition_given_pos']*100:.2f}%)")
                st.caption(f"Numerator: <span style='color:{fp_color}'>■</span> {categories[1]['label']}", unsafe_allow_html=True)
                st.caption(f"Denominator: All Test+ cases ({bayes_calc['test_positive']} total)")
            
            # Key insight box
            st.info(f"""
            **Key Insight:** Even if the test is positive, the probability of actually having the condition is {bayes_calc['posterior_condition_given_pos']*100:.1f}%. 
            This happens because the condition is rare (prior = {bayes_calc['prior_condition']*100:.1f}%), so false positives 
            ({bayes_calc['FP']}) outnumber true positives ({bayes_calc['TP']}).
            """)

else:
    # Show example/default state
    st.info("👈 Configure your visualization settings in the sidebar and click 'Generate Visualization'")
    
    # Show example use cases
    st.subheader("📚 Example Use Cases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Bayes' Rule Example:**
        - Total: 1000 people
        - Grid: 25×40 (1000 cells)
        - Categories:
          - "Has Disease & Tests Positive": 9
          - "No Disease & Tests Positive": 99
          - "Has Disease & Tests Negative": 1
          - "No Disease & Tests Negative": 891
        
        This visualizes the counterintuitive result that even with a 90% accurate test,
        a positive result might only indicate a 9% chance of actually having a rare disease.
        """)
    
    with col2:
        st.markdown("""
        **Simple Probability:**
        - Total: 100 people
        - Grid: 10×10 (100 cells)
        - Categories:
          - "Event A": 25 (25%)
          - "Event B": 35 (35%)
          - "Neither": 40 (40%)
        
        Perfect for introducing basic probability concepts with tangible whole numbers
        that students can count and relate to.
        """)

# Footer
st.markdown("---")
st.markdown("""
**Tips:**
- Keep grid dimensions that multiply to your total number for best results
- Use shuffle to show random distribution vs. grouped distribution
- Try different shapes (squares vs circles) for visual variety
- Colors can be customized for each category
""")
