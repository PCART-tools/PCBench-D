def _categorize(categories, df):
    """ Categorize columns in dataframe

    >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': [0, 2, 0]})
    >>> categories = {'y': ['A', 'B', 'c']}
    >>> _categorize(categories, df)
       x  y
    0  1  A
    1  2  c
    2  3  A

    >>> _categorize(categories, df.y)
    0    A
    1    c
    2    A
    dtype: category
    Categories (3, object): [A, B, c]
    """
    if '.index' in categories:
        index = pd.CategoricalIndex(
                  pd.Categorical.from_codes(df.index.values, categories['.index']))
    else:
        index = df.index
    if isinstance(df, pd.Series):
        if df.name in categories:
            cat = pd.Categorical.from_codes(df.values, categories[df.name])
            return pd.Series(cat, index=index)
        else:
            return df

    else:
        return pd.DataFrame(
                dict((col, pd.Categorical.from_codes(df[col].values, categories[col])
                           if col in categories
                           else df[col].values)
                    for col in df.columns),
                columns=df.columns,
                index=index)
