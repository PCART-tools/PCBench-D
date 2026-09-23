def _xl_rowcols_to_range(*row_col_pairs: int) -> list[str]:
    """Return list of "A1:B2" range refs from pairs of row/col indexes."""
    from xlsxwriter.utility import xl_rowcol_to_cell

    cell_refs = (xl_rowcol_to_cell(row, col) for row, col in _cluster(row_col_pairs))
    return [f"{cell_start}:{cell_end}" for cell_start, cell_end in _cluster(cell_refs)]
