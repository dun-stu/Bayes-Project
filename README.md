# Bayes-Project

A flexible software tool to help non-mathematicians understand probability. The tool generates customizable graphical displays (grids, colors, shapes) that illustrate concepts like Bayes' rule using whole numbers (e.g., "80 out of 400") instead of abstract percentages.

## Features

- 🎨 **Interactive Visualization**: Create colorful grid-based visualizations of probability concepts
- 🔢 **Whole Numbers**: Use concrete numbers instead of abstract percentages
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
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## How to Use

1. **Set Total Number**: Enter the total number of items to visualize (e.g., 400)
2. **Configure Grid**: Set the number of rows and columns (e.g., 20×20 = 400)
3. **Add Categories**: 
   - Specify the number of categories
   - For each category, enter:
     - Label (name)
     - Count (how many items)
     - Color (visual representation)
4. **Customize Display**:
   - Choose cell shape (Square or Circle)
   - Toggle grid lines, legend, and statistics
   - Option to shuffle for random distribution
5. **Generate**: Click "Generate Visualization" to create your probability grid

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

