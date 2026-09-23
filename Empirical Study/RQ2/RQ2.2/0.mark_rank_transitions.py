"""Mark large adjacent-version rank changes in column K.

The source JSON is read from column H.  For every adjacent pair in its
``order`` list, the script checks all methods in the version payload.  A
transition is recorded only when the previous version's ``total`` is at least
10 and a method changes rank by at least 10% of that total.  Multiple
qualifying transitions are joined with commas in the same K cell.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from openpyxl import load_workbook


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILES = [
    BASE_DIR / "input" / "fix_D.xlsx",
    BASE_DIR / "input" / "fix_R.xlsx",
]
H_COLUMN = 8
K_COLUMN = 11
THRESHOLD_RATIO = 0.10
MIN_PREVIOUS_TOTAL = 10


def _method_names(payload: dict[str, Any], methods_cell: Any) -> list[str]:
    """Return the methods to inspect, preserving the worksheet's order."""
    if isinstance(methods_cell, str) and methods_cell.strip():
        methods = [item.strip() for item in methods_cell.split(",") if item.strip()]
        if methods:
            return methods

    order = payload.get("order", [])
    if not order:
        return []
    first_version = payload.get(order[0], {})
    return list(first_version.keys())


def qualifying_transitions(
    cell_value: Any,
    methods_cell: Any,
    threshold_ratio: float = THRESHOLD_RATIO,
    min_previous_total: int = MIN_PREVIOUS_TOTAL,
) -> list[str]:
    """Find adjacent version transitions with a large rank change.

    A transition is included once even if multiple methods qualify for the
    same adjacent version pair.
    """
    if not isinstance(cell_value, str) or not cell_value.strip():
        return []

    try:
        payload = json.loads(cell_value)
    except json.JSONDecodeError:
        # Other worksheets or header rows may contain ordinary text in H.
        return []

    if not isinstance(payload, dict):
        return []

    order = payload.get("order", [])
    if not isinstance(order, list) or len(order) < 2:
        return []

    methods = _method_names(payload, methods_cell)
    result: list[str] = []

    for previous_version, current_version in zip(order, order[1:]):
        previous_data = payload.get(previous_version, {})
        current_data = payload.get(current_version, {})
        qualifies = False

        for method in methods:
            previous = previous_data.get(method)
            current = current_data.get(method)
            if not isinstance(previous, dict) or not isinstance(current, dict):
                continue

            previous_rank = previous.get("rank")
            current_rank = current.get("rank")
            previous_total = previous.get("total")
            if not all(
                isinstance(value, (int, float))
                for value in (previous_rank, current_rank, previous_total)
            ):
                continue

            rank_change = abs(current_rank - previous_rank)
            if previous_total < min_previous_total:
                continue
            if rank_change >= previous_total * threshold_ratio:
                qualifies = True
                break

        if qualifies:
            result.append(f"{previous_version}->{current_version}")

    return result


def mark_workbook(
    input_path: Path,
    output_path: Path,
    threshold_ratio: float = THRESHOLD_RATIO,
    min_previous_total: int = MIN_PREVIOUS_TOTAL,
) -> int:
    """Read H and write results to K on every worksheet and row."""
    workbook = load_workbook(input_path)
    marked_rows = 0

    for worksheet in workbook.worksheets:
        for row in range(1, worksheet.max_row + 1):
            transitions = qualifying_transitions(
                worksheet.cell(row, H_COLUMN).value,
                worksheet.cell(row, 9).value,
                threshold_ratio,
                min_previous_total,
            )
            worksheet.cell(row, K_COLUMN).value = ", ".join(transitions)
            if transitions:
                marked_rows += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)
    return marked_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Input workbook containing JSON in column H. Defaults to input/fix_D.xlsx and input/fix_R.xlsx.",
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=THRESHOLD_RATIO,
        help="Rank-change threshold as a fraction of the previous total (default: 0.1).",
    )
    parser.add_argument(
        "--min-total",
        type=int,
        default=MIN_PREVIOUS_TOTAL,
        help="Exclude transitions whose previous version total is below this value (default: 10).",
    )
    args = parser.parse_args()

    inputs = [args.input] if args.input else INPUT_FILES
    for input_path in inputs:
        marked_rows = mark_workbook(
            input_path,
            input_path,
            args.ratio,
            args.min_total,
        )
        print(f"Saved: {input_path}")
        print(f"Rows with at least one qualifying transition: {marked_rows}")


if __name__ == "__main__":
    main()
