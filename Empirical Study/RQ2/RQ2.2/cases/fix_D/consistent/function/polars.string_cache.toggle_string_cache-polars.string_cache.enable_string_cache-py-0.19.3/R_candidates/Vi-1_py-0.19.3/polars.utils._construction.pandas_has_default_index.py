def pandas_has_default_index(df: pd.DataFrame) -> bool:
    """Identify if the pandas frame only has a default (or equivalent) index."""
    from pandas.core.indexes.range import RangeIndex

    index_cols = df.index.names

    if len(index_cols) > 1 or index_cols not in ([None], [""]):
        # not default: more than one index, or index is named
        return False
    elif df.index.equals(RangeIndex(start=0, stop=len(df), step=1)):
        # is default: simple range index
        return True
    else:
        # finally, is the index _equivalent_ to a default unnamed
        # integer index with frame data that was previously sorted
        return (
            str(df.index.dtype).startswith("int")
            and (df.index.sort_values() == np.arange(len(df))).all()
        )
