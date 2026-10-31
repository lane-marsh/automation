"""Command-line interface for the automation tools."""

import argparse
import csv
from pathlib import Path

from lane_automation.ml import BayesCat


_DEFAULT_EXAMPLE_CSV = (
    Path(__file__).resolve().parent.parent
    / "example_data"
    / "example_produce_data.csv"
)


def _read_training_data(path, category_column, text_column):
    categories = []
    descriptions = []

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no header row.")
        if category_column not in reader.fieldnames:
            raise ValueError("CSV is missing category column {!r}.".format(category_column))
        if text_column not in reader.fieldnames:
            raise ValueError("CSV is missing text column {!r}.".format(text_column))

        for line_number, row in enumerate(reader, start=2):
            category = row.get(category_column)
            description = row.get(text_column)
            if category is None or description is None:
                raise ValueError("CSV row {} does not have the expected columns.".format(line_number))
            if not category.strip() or not description.strip():
                raise ValueError("CSV row {} has an empty category or description.".format(line_number))
            categories.append(category)
            descriptions.append(description)

    if not categories:
        raise ValueError("CSV has no training rows.")
    return categories, descriptions


def _classify(args, parser):
    try:
        categories, descriptions = _read_training_data(
            args.csv_file, args.category_column, args.text_column
        )
    except (OSError, csv.Error, ValueError) as error:
        parser.error(str(error))

    classifier = BayesCat(
        categories,
        descriptions,
        benign_words=args.ignore_word,
    )
    category = classifier.guess(args.text)
    if not category:
        print("No matching category found.")
        return 1
    print(category)
    return 0


def _interactive(args, parser):
    try:
        categories, descriptions = _read_training_data(
            args.csv_file, args.category_column, args.text_column
        )
    except (OSError, csv.Error, ValueError) as error:
        parser.error(str(error))

    classifier = BayesCat(
        categories,
        descriptions,
        benign_words=args.ignore_word,
    )
    print("Enter a description to classify. Submit a blank line to quit.")
    while True:
        try:
            description = input("Description: ")
        except EOFError:
            print()
            return 0
        if not description.strip():
            return 0

        category = classifier.guess(description)
        if category:
            print("Prediction: {}".format(category))
        else:
            print("No matching category found.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="lane-tools",
        description="Run tools from the lane-automation collection.",
    )
    commands = parser.add_subparsers(dest="tool", required=True)
    ml_parser = commands.add_parser("ml", help="machine-learning tools")
    ml_commands = ml_parser.add_subparsers(dest="ml_command", required=True)
    classify_parser = ml_commands.add_parser(
        "classify",
        help="classify text using labeled rows from a CSV file",
    )
    classify_parser.add_argument("csv_file", type=Path, help="training CSV file")
    classify_parser.add_argument("text", help="text to classify")
    classify_parser.add_argument(
        "--category-column",
        required=True,
        help="CSV column containing category labels",
    )
    classify_parser.add_argument(
        "--text-column",
        required=True,
        help="CSV column containing training descriptions",
    )
    classify_parser.add_argument(
        "--ignore-word",
        action="append",
        default=[],
        help="word to ignore when matching (can be specified more than once)",
    )
    classify_parser.set_defaults(handler=_classify)

    interactive_parser = ml_commands.add_parser(
        "interactive",
        help="prompt for descriptions and classify them using a CSV file",
    )
    interactive_parser.add_argument(
        "csv_file",
        nargs="?",
        type=Path,
        default=_DEFAULT_EXAMPLE_CSV,
        help="training CSV file (defaults to the included produce example)",
    )
    interactive_parser.add_argument(
        "--category-column",
        default="produce",
        help="CSV column containing category labels (default: produce)",
    )
    interactive_parser.add_argument(
        "--text-column",
        default="description",
        help="CSV column containing training descriptions (default: description)",
    )
    interactive_parser.add_argument(
        "--ignore-word",
        action="append",
        default=["this", "the", "is"],
        help="word to ignore when matching (can be specified more than once)",
    )
    interactive_parser.set_defaults(handler=_interactive)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args, parser)
