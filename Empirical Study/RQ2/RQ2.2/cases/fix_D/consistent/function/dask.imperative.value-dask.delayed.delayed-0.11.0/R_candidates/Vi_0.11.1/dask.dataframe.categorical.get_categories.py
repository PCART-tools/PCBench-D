def get_categories(df):
    """
    Get Categories of dataframe

    >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': ['A', 'B', 'A']})
    >>> df['y'] = df.y.astype('category')
    >>> get_categories(df)
    {'y': Index([u'A', u'B'], dtype='object')}
    """
    result = dict((col, df[col].cat.categories) for col in df.columns
                  if is_categorical_dtype(df[col]))
    if is_categorical_dtype(df.index):
        result['.index'] = df.index.categories
    return result
