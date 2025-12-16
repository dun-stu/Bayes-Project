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
from scenarios import get_all_scenarios, get_scenario_by_name

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

# Scenario Selection
st.sidebar.subheader("Select Scenario")
scenario_options = ["Custom"] + [s.name for s in get_all_scenarios()]
selected_scenario_name = st.sidebar.selectbox(
    "Choose a pre-configured scenario or create your own",
    options=scenario_options,
    index=0,
    key="scenario_selector"
)

# Load selected scenario if not Custom
selected_scenario = None
if selected_scenario_name != "Custom":
    selected_scenario = get_scenario_by_name(selected_scenario_name)
    if selected_scenario:
        st.sidebar.info(f"**{selected_scenario.title}**\n\n{selected_scenario.description}")

st.sidebar.markdown("---")

# Input 1: Total whole number
default_total = selected_scenario.total if selected_scenario else 400
total_number = st.sidebar.number_input(
    "Total Number of Items",
    min_value=1,
    max_value=10000,
    value=default_total,
    step=1,
    help="Total number of items to visualize (e.g., 400)",
    disabled=(selected_scenario is not None)
)

# Input 2: Grid layout
st.sidebar.subheader("Grid Layout")
default_rows = selected_scenario.rows if selected_scenario else 20
default_cols = selected_scenario.cols if selected_scenario else 20
col1, col2 = st.sidebar.columns(2)
with col1:
    grid_rows = st.number_input(
        "Rows",
        min_value=1,
        max_value=100,
        value=default_rows,
        step=1,
        disabled=(selected_scenario is not None)
    )
with col2:
    grid_cols = st.number_input(
        "Columns",
        min_value=1,
        max_value=100,
        value=default_cols,
        step=1,
        disabled=(selected_scenario is not None)
    )

# Verify grid matches total
grid_total = grid_rows * grid_cols
if grid_total != total_number:
    st.sidebar.warning(f"⚠️ Grid size ({grid_rows}×{grid_cols}={grid_total}) doesn't match total ({total_number})")
    st.sidebar.info(f"Suggested: {int(np.sqrt(total_number))}×{int(np.sqrt(total_number))} = {int(np.sqrt(total_number))**2}")

# Input 3: Proportions and labels
st.sidebar.subheader("Categories")

# Default colors
default_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                  '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']

categories = []
total_proportion = 0

if selected_scenario:
    # Use scenario categories
    for cat in selected_scenario.categories:
        categories.append({
            'label': cat.label,
            'count': cat.count,
            'color': cat.color
        })
        total_proportion += cat.count
    
    # Display categories (read-only)
    for i, category in enumerate(categories):
        st.sidebar.markdown(f"**Category {i+1}**: {category['label']} ({category['count']})")
else:
    # Custom mode - manual input
    num_categories = st.sidebar.number_input(
        "Number of Categories",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        help="How many different categories to visualize"
    )
    
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
        
        # Bayesian calculation for Medical Screening scenario
        if selected_scenario_name == "Medical Screening":
            st.markdown("---")
            st.markdown("### 🎯 Bayesian Analysis")
            
            # Find the relevant categories by label
            true_positives = 0
            false_positives = 0
            for category in categories:
                if "Has Disease & Tests Positive" in category['label']:
                    true_positives = category['count']
                elif "No Disease & Tests Positive" in category['label']:
                    false_positives = category['count']
            
            all_positives = true_positives + false_positives
            
            if all_positives > 0:
                probability_disease_given_positive = (true_positives / all_positives) * 100
                st.success(f"""
                **Key Insight: Probability of Having Disease Given Positive Test**
                
                P(Disease | Positive Test) = True Positives / All Positives
                
                = {true_positives} / ({true_positives} + {false_positives})
                
                = {true_positives} / {all_positives}
                
                = **{probability_disease_given_positive:.2f}%**
                
                Even though the test is 90% accurate, if you test positive, there's only a {probability_disease_given_positive:.1f}% chance you actually have the disease! This is because false positives ({false_positives}) greatly outnumber true positives ({true_positives}) when the disease is rare.
                """)
        
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
