# Lane Automation

A collection of practical Python utilities, with a unified command-line
interface for running tools.

## Install for development

From this directory, install the project in editable mode:

```sh
python3 -m pip install -e .
```

This installs the `lane-tools` command and makes local source changes available
without reinstalling.

## Classify text from a CSV

The classifier expects one CSV column with category labels and another with
training descriptions:

```sh
lane-tools ml classify example_data/example_produce_data.csv \
  "green vegetable" \
  --category-column produce \
  --text-column description \
  --ignore-word this \
  --ignore-word is
```

The command prints the best-matching category. Use `lane-tools --help` or
`lane-tools ml classify --help` for usage details. It can also be run with
`python3 -m lane_automation`.

## Interactive classification

Start a prompt that loads the included produce example CSV by default:

```sh
lane-tools ml interactive
```

Enter a description at each prompt; submit a blank line or press Ctrl+D to
finish. To use another CSV, pass its path and optionally set the column names:

```sh
lane-tools ml interactive path/to/training.csv \
  --category-column category \
  --text-column description
```

## Python API

The reusable modules live in functional packages and can be imported directly:

```python
from lane_automation.data import ObjectifyCSV, ObjectifyXL
from lane_automation.games import Player, PokerGame, TexasHoldEm
from lane_automation.ml import BayesCat
```

`ObjectifyXL` uses `openpyxl`. The CLI currently exposes the classifier; data
and game tools can be added as CLI subcommands independently.

The original top-level module imports remain available for compatibility:
`from ml_objects import BayesCat`, `from dataCrunch import ObjectifyCSV`, and
`from poker import Player`. New code should prefer the `lane_automation`
package imports shown above.

## Tests

Run the command-line tests with:

```sh
python3 -m unittest discover -s tests
```