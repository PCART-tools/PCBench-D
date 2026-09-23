def _is_aligned(df, by):
    """Check if `df` and `by` have aligned indices"""
    if isinstance(by, (pd.Series, pd.DataFrame)):
        return df.index.equals(by.index)
    elif isinstance(by, (list, tuple)):
        return all(_is_aligned(df, i) for i in by)
    else:
        return True
