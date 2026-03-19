import unittest

from calculations import BayesianParameters, compute
from frequency_tree import create_frequency_tree
from icon_array import compute_grid, create_icon_array
from scenarios import SCENARIOS
from text_layer import generate_bayes_explanation, generate_problem_text


class BayesianToolTests(unittest.TestCase):
    @staticmethod
    def _get_mammography_scenario():
        return next((s for s in SCENARIOS if s["id"] == "mammography"), None)

    def test_mammography_defaults(self):
        params = BayesianParameters(N=1000, base_rate=0.01, sensitivity=0.90, fpr=0.09)
        counts = compute(params)
        self.assertEqual(counts.n_disease, 10)
        self.assertEqual(counts.n_healthy, 990)
        self.assertEqual(counts.true_positive, 9)
        self.assertEqual(counts.false_negative, 1)
        self.assertEqual(counts.false_positive, 89)
        self.assertEqual(counts.true_negative, 901)
        self.assertEqual(counts.total_test_positive, 98)
        self.assertAlmostEqual(counts.posterior_ppv, 9 / 98, places=6)

    def test_grid_capacity(self):
        rows, cols = compute_grid(1000)
        self.assertGreaterEqual(rows * cols, 1000)

    def test_text_generation_framings(self):
        scenario = self._get_mammography_scenario()
        self.assertIsNotNone(scenario)
        params = BayesianParameters(**scenario["defaults"])
        counts = compute(params)

        freq = generate_problem_text(counts, params, scenario["domain"], "frequency")
        self.assertIn("Imagine", freq["description"])
        self.assertIn("Of all those who", freq["question"])

        prob = generate_problem_text(counts, params, scenario["domain"], "probability")
        self.assertIn("prevalence", prob["description"].lower())
        self.assertIn("P(Condition | Test⁺)", prob["question"])

    def test_visual_functions_return_figures(self):
        scenario = self._get_mammography_scenario()
        self.assertIsNotNone(scenario)
        params = BayesianParameters(**scenario["defaults"])
        counts = compute(params)

        icon_fig = create_icon_array(counts, scenario["domain"], "frequency", "condition")
        tree_fig = create_frequency_tree(counts, params, scenario["domain"], "frequency", "frequency_tree")

        icon_dict = icon_fig.to_dict()
        tree_dict = tree_fig.to_dict()
        rows, cols = compute_grid(counts.N)

        self.assertEqual(icon_dict["data"][0]["type"], "scatter")
        self.assertEqual(icon_dict["data"][0]["marker"]["symbol"], "square")
        total_points = sum(len(trace.get("x", [])) for trace in icon_dict["data"])
        self.assertEqual(total_points, rows * cols)
        self.assertEqual(len(icon_dict["layout"].get("annotations", [])), 0)
        self.assertEqual(icon_dict["layout"]["legend"]["orientation"], "h")
        self.assertGreater(icon_dict["layout"]["legend"]["y"], 1.0)
        self.assertTrue(
            any(
                isinstance(trace.get("name"), str) and "True Positive" in trace["name"]
                for trace in icon_dict["data"]
            )
        )

        self.assertGreaterEqual(len(tree_dict["layout"]["shapes"]), 10)
        self.assertTrue(
            any("PPV:" in annotation["text"] for annotation in tree_dict["layout"]["annotations"])
        )

    def test_bayes_explanation_generation(self):
        scenario = self._get_mammography_scenario()
        self.assertIsNotNone(scenario)
        params = BayesianParameters(**scenario["defaults"])
        counts = compute(params)

        freq = generate_bayes_explanation(counts, params, scenario["domain"], "frequency")
        self.assertIn("True Positives", freq["formula"])
        self.assertIn("9 / (9 + 89)", freq["substitution"])
        self.assertEqual(len(freq["mapping"]), 4)

        prob = generate_bayes_explanation(counts, params, scenario["domain"], "probability")
        self.assertIn("P(Condition | Test⁺)", prob["formula"])
        self.assertIn("= 0.092", prob["substitution"])
        self.assertTrue(any("Frequency Tree" in item for item in prob["mapping"]))
        self.assertIn(r"P(D \mid T^+)", prob["latex_original"])
        self.assertIn(r"P(T^+ \mid \neg D)\,P(\neg D)", prob["latex_expanded"])
        self.assertIn(r"= 0.092", prob["latex_substitution"])
        self.assertEqual(len(prob["term_mapping"]), 3)


if __name__ == "__main__":
    unittest.main()
