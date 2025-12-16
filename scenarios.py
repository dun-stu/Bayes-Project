"""
Scenario Library for Probability Visualization
Defines pre-configured scenarios for teaching probability concepts.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Category:
    """Represents a category in a probability scenario."""
    label: str
    count: int
    color: str


@dataclass
class Scenario:
    """Represents a complete probability scenario with all configuration."""
    name: str
    title: str
    description: str
    total: int
    rows: int
    cols: int
    categories: List[Category]
    
    def to_dict(self) -> Dict:
        """Convert scenario to dictionary format."""
        return {
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'total': self.total,
            'rows': self.rows,
            'cols': self.cols,
            'categories': [
                {
                    'label': cat.label,
                    'count': cat.count,
                    'color': cat.color
                }
                for cat in self.categories
            ]
        }


# Pre-defined scenarios
MEDICAL_SCREENING = Scenario(
    name="Medical Screening",
    title="Bayes' Rule: Medical Screening Example",
    description="""This scenario demonstrates why a positive medical test doesn't always mean you have the disease.
    
Consider a rare disease that affects 1% of the population, with a test that is 90% accurate:
- 10 people have the disease (1% of 1000)
- 9 test positive (90% of those with disease) - TRUE POSITIVES
- 1 tests negative (10% false negative)
- 990 people don't have the disease (99% of 1000)
- 99 test positive (10% false positive rate) - FALSE POSITIVES
- 891 test negative (90% true negative)

**Key Insight**: If you test positive, the probability you actually have the disease is only 9/(9+99) = 8.3%!
This is because false positives outnumber true positives when the disease is rare.""",
    total=1000,
    rows=25,
    cols=40,
    categories=[
        Category(label="Has Disease & Tests Positive", count=9, color="#FF6B6B"),
        Category(label="No Disease & Tests Positive", count=99, color="#FFA07A"),
        Category(label="Has Disease & Tests Negative", count=1, color="#4ECDC4"),
        Category(label="No Disease & Tests Negative", count=891, color="#45B7D1"),
    ]
)

SIMPLE_PROBABILITY = Scenario(
    name="Simple Probability",
    title="Basic Probability with Students",
    description="""A simple example for introducing basic probability concepts with tangible whole numbers.

In a class of 100 students:
- 25 students are in Category A (25%)
- 35 students are in Category B (35%)
- 40 students are in neither category (40%)

This makes it easy to understand probability as "how many out of the total" rather than abstract percentages.""",
    total=100,
    rows=10,
    cols=10,
    categories=[
        Category(label="Event A", count=25, color="#FF6B6B"),
        Category(label="Event B", count=35, color="#4ECDC4"),
        Category(label="Neither", count=40, color="#45B7D1"),
    ]
)

COIN_FLIP = Scenario(
    name="Coin Flip",
    title="Coin Flip Distribution",
    description="""Visualize experimental vs. theoretical probability with coin flips.

400 coin flips showing a typical experimental outcome:
- Heads: 203 flips (50.75%)
- Tails: 197 flips (49.25%)

This demonstrates that experimental results may differ slightly from the theoretical 50/50 probability,
but approach it as the number of trials increases.""",
    total=400,
    rows=20,
    cols=20,
    categories=[
        Category(label="Heads", count=203, color="#FFD700"),
        Category(label="Tails", count=197, color="#C0C0C0"),
    ]
)


def get_all_scenarios() -> List[Scenario]:
    """Return all available pre-defined scenarios."""
    return [MEDICAL_SCREENING, SIMPLE_PROBABILITY, COIN_FLIP]


def get_scenario_by_name(name: str) -> Scenario:
    """Get a specific scenario by name."""
    scenarios = get_all_scenarios()
    for scenario in scenarios:
        if scenario.name == name:
            return scenario
    return None


def get_scenario_names() -> List[str]:
    """Return list of all scenario names."""
    return [scenario.name for scenario in get_all_scenarios()]
