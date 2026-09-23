def _xl_table_formula(df: DataFrame, cols: Iterable[str], func: str) -> str:
    """Return a formula using structured references to columns in a named table."""
    m: dict[str, Any] = {}
    if isinstance(cols, str):
        cols = [cols]
    if _adjacent_cols(df, cols, min_max=m):
        return f"={func.upper()}([@[{m['min']['name']}]:[{m['max']['name']}]])"
    else:
        colrefs = ",".join(f"[@[{c}]]" for c in cols)
        return f"={func.upper()}({colrefs})"
