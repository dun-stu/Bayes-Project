# Bayes-Project

An interactive Streamlit teaching tool for Bayesian reasoning. The app uses natural-frequency counts and Plotly visualizations to make Bayes' rule tractable for learners.

## Features

- 🎲 **Scenario library**: Built-in examples (mammography, COVID rapid test, spam filter, and more) plus custom settings
- 🔢 **Natural-frequency framing**: Concrete statements like “9 out of 98”
- 📉 **Probability framing**: Formal notation like `P(D|T⁺)`
- 🟦🟧 **Two coordinated visualizations**:
  - Plotly icon array (with regroup by test result toggle)
  - Plotly frequency/probability tree
- ⚡ **Reactive updates**: All text, charts, and posterior update immediately as parameters change

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

1. Select a scenario (or **Custom**) in the sidebar.
2. Adjust parameters:
   - Population size `N`
   - Base rate (prevalence)
   - Sensitivity
   - False positive rate
3. Toggle **Show as probabilities** to switch the full app framing.
4. Use tabs to switch between **Icon Array** and **Frequency Tree**.
5. Use chart-specific toggles:
   - **Group by test result** (icon array)
   - **Show as probability tree** (tree view)

## Requirements

- Python 3.7+
- Streamlit 1.28.0+
- NumPy 1.24.0+
- Plotly 5.18.0+

## License

This project is open source and available for educational purposes.
