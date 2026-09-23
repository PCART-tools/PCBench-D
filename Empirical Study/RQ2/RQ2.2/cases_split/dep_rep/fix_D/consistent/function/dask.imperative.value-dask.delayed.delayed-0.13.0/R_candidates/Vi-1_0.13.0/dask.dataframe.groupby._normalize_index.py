def _normalize_index(df, index):
    """Replace series with column names in an index wherever possible.
    """
    if not isinstance(df, DataFrame):
        return index

    elif isinstance(index, list):
        return [_normalize_index(df, col) for col in index]

    elif (isinstance(index, Series) and index.name in df.columns and
          index._name == df[index.name]._name):
            return index.name

    elif (isinstance(index, DataFrame) and
          set(index.columns).issubset(df.columns) and
          index._name == df[index.columns]._name):
        return list(index.columns)

    else:
        return index
