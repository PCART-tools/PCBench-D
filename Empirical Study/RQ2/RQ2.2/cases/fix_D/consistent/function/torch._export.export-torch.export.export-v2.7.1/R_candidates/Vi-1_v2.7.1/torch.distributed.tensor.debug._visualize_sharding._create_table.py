def _create_table(blocks):
    """
    Creates a tabulate table given row and column ranges with device name
    """
    try:
        from tabulate import tabulate
    except ImportError as e:
        raise ImportError("tabulate package is required to visualize sharding") from e

    # Extract unique row and column ranges
    row_ranges = sorted({block["row_range"] for block in blocks})
    col_ranges = sorted({block["column_range"] for block in blocks})

    # Create a matrix initialized with empty strings
    matrix = [["" for _ in col_ranges] for _ in row_ranges]

    # Fill the matrix with values
    for block in blocks:
        row_index = row_ranges.index(block["row_range"])
        col_index = col_ranges.index(block["column_range"])
        if matrix[row_index][col_index] == "":
            matrix[row_index][col_index] = block["value"]
        else:
            matrix[row_index][col_index] += ", " + block["value"]

    # Prepare headers
    row_headers = [f"Row {r[0]}-{r[1]}" for r in row_ranges]
    col_headers = [f"Col {c[0]}-{c[1]}" for c in col_ranges]

    return tabulate(matrix, headers=col_headers, showindex=row_headers)
