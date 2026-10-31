import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from lane_automation.cli import main
from dataCrunch import ObjectifyCSV as LegacyObjectifyCSV
from lane_automation.data import ObjectifyCSV
from lane_automation.games import Player
from lane_automation.ml import BayesCat
from ml_objects import BayesCat as LegacyBayesCat
from poker import Player as LegacyPlayer


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class CompatibilityImportTests(unittest.TestCase):
    def test_legacy_modules_reexport_package_classes(self):
        self.assertIs(LegacyObjectifyCSV, ObjectifyCSV)
        self.assertIs(LegacyBayesCat, BayesCat)
        self.assertIs(LegacyPlayer, Player)


class ClassifyCommandTests(unittest.TestCase):
    def test_classifies_text_from_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "produce.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["produce", "description"])
                writer.writerow(["apple", "this fruit is red"])
                writer.writerow(["broccoli", "this vegetable is green"])

            output = io.StringIO()
            with redirect_stdout(output):
                result = main([
                    "ml",
                    "classify",
                    str(csv_path),
                    "green vegetable",
                    "--category-column",
                    "produce",
                    "--text-column",
                    "description",
                    "--ignore-word",
                    "this",
                    "--ignore-word",
                    "is",
                ])

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "broccoli\n")

    def test_interactive_command_uses_example_and_prompts_until_blank(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["green vegetable", ""]):
            with redirect_stdout(output):
                result = main(["ml", "interactive"])

        self.assertEqual(result, 0)
        self.assertIn("Prediction: broccoli", output.getvalue())
        self.assertIn("blank line to quit", output.getvalue())

    def test_interactive_command_exits_cleanly_on_eof(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(output):
                result = main([
                    "ml",
                    "interactive",
                    str(PROJECT_ROOT / "example_data" / "example_produce_data.csv"),
                ])

        self.assertEqual(result, 0)
        self.assertTrue(output.getvalue().endswith("\n"))


if __name__ == "__main__":
    unittest.main()
