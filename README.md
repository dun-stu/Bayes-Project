# Bayes-Project

A flexible software tool to help non-mathematicians understand probability. The tool generates customizable graphical displays (grids, colors, shapes) that illustrate concepts like Bayes' rule using whole numbers (e.g., "80 out of 400") instead of abstract percentages.

## Features

- 🎨 **Interactive Visualization**: Create colorful grid-based visualizations of probability concepts
- 🔢 **Whole Numbers**: Use concrete numbers instead of abstract percentages
- 📚 **Scenario Library**: Pre-built teaching scenarios with guided Bayes' theorem calculations
- 📊 **Flexible Configuration**: Customize grid size, categories, colors, and shapes
- 📈 **Statistics Display**: View counts, percentages, and odds for each category
- 🎲 **Teaching Tool**: Perfect for classroom demonstrations of Bayes' rule and probability

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dun-stu/Bayes-Project.git
cd Bayes-Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
python streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## How to Use

### Using Pre-built Scenarios

1. **Select a Scenario**: Choose from the "Scenario" dropdown in the sidebar:
   - **Rare Disease Test**: Classic medical testing example with a 1% disease prevalence
   - **Spam Filter**: Email classification scenario
   - **Security Screening**: Airport security threat detection
   - **Drug Test**: Workplace drug testing scenario
   - **Custom (manual)**: Create your own custom visualization

2. **View the Scenario**: The scenario description and all parameters are automatically loaded

3. **Generate Visualization**: Click "Generate Visualization" to see the probability grid

4. **Explore Bayes Calculations**: For pre-built scenarios, you'll see detailed calculations including:
   - **Prior Probabilities**: P(Condition) and P(No Condition)
   - **Likelihoods**: P(Test+ | Condition), P(Test+ | No Condition), etc.
   - **Posteriors (Bayes' Rule)**: P(Condition | Test+) - the key insight!

### Creating Custom Visualizations

1. **Select Custom Mode**: Choose "Custom (manual)" from the Scenario dropdown

2. **Set Total Number**: Enter the total number of items to visualize (e.g., 400)

3. **Configure Grid**: Set the number of rows and columns (e.g., 20×20 = 400)

4. **Add Categories**: 
   - Specify the number of categories
   - For each category, enter:
     - Label (name)
     - Count (how many items)
     - Color (visual representation)

5. **Customize Display**:
   - Choose cell shape (Square or Circle)
   - Toggle grid lines, legend, and statistics
   - Option to shuffle for random distribution

6. **Generate**: Click "Generate Visualization" to create your probability grid

## Scenario Library & Guided Bayes Examples

The app includes pre-built scenarios that demonstrate Bayes' theorem with realistic examples. Each scenario:

- **Automatically configures** the grid, categories, and colors
- **Shows the visualization** with four mutually exclusive categories (True Positive, False Positive, False Negative, True Negative)
- **Calculates and displays**:
  - **Priors**: The base rate probability of having the condition (e.g., P(Disease) = 1%)
  - **Likelihoods**: Test accuracy rates (e.g., P(Test+ | Disease) = 90%)
  - **Posteriors**: The probability you care about (e.g., P(Disease | Test+) = 8.3%)

### Understanding the Calculations

Each calculation is shown with:
- **Whole number counts**: e.g., "9 / 108"
- **Decimal probability**: e.g., "≈ 0.083"
- **Percentage**: e.g., "(8.3%)"
- **Visual reference**: Which colored grid cells are being counted

The **Key Insight** box explains the often counterintuitive result: even with an accurate test, a positive result might have a low probability of indicating the actual condition when the condition is rare.

### Switching Between Modes

- **To use a scenario**: Select it from the "Scenario" dropdown
- **To customize**: Select "Custom (manual)" from the dropdown
- **All manual controls remain available** in custom mode

## Example Use Cases

### Bayes' Rule Example

Demonstrate why a positive medical test doesn't always mean you have the disease:

- **Total**: 1000 people
- **Grid**: 25×40
- **Categories**:
  - Has Disease & Tests Positive: 9 (0.9%)
  - No Disease & Tests Positive: 99 (9.9%)
  - Has Disease & Tests Negative: 1 (0.1%)
  - No Disease & Tests Negative: 891 (89.1%)

This shows that even with a 90% accurate test, a positive result might only indicate a 9% actual chance of having a rare disease.

### Simple Probability

Teach basic probability with tangible numbers:

- **Total**: 100 students
- **Grid**: 10×10
- **Categories**:
  - Likes Math: 35 students (35%)
  - Likes Science: 45 students (45%)
  - Likes Both: 20 students (20%)

### Coin Flip Distribution

Show experimental vs. theoretical probability:

- **Total**: 400 flips
- **Grid**: 20×20
- **Categories**:
  - Heads: 203 (50.75%)
  - Tails: 197 (49.25%)

## Requirements

- Python 3.7+
- Streamlit 1.28.0+
- NumPy 1.24.0+
- Matplotlib 3.7.0+

## License

This project is open source and available for educational purposes.

