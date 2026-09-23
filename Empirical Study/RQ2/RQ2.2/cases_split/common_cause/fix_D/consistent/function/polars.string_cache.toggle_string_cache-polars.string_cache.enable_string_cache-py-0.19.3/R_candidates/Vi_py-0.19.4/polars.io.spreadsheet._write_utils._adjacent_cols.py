def _adjacent_cols(df: DataFrame, cols: Iterable[str], min_max: dict[str, Any]) -> bool:
    """Indicate if the given columns are all adjacent to one another."""
    idxs = sorted(df.find_idx_by_name(col) for col in cols)
    if idxs != sorted(range(min(idxs), max(idxs) + 1)):
        return False
    else:
        columns = df.columns
        min_max["min"] = {"idx": idxs[0], "name": columns[idxs[0]]}
        min_max["max"] = {"idx": idxs[-1], "name": columns[idxs[-1]]}
        return True
