def _categorize_block(df, categories, index):
    """ Categorize a dataframe with given categories

    df: DataFrame
    categories: dict mapping column name to iterable of categories
    """
    df = df.copy()
    for col, vals in categories.items():
        if is_categorical_dtype(df[col]):
            df[col] = df[col].cat.set_categories(vals)
        else:
            df[col] = pd.Categorical(df[col], categories=vals, ordered=False)
    if index is not None:
        if is_categorical_dtype(df.index):
            ind = df.index.set_categories(index)
        else:
            ind = pd.Categorical(df.index, categories=index, ordered=False)
        ind.name = df.index.name
        df.index = ind
    return df
