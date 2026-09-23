def strip_categories(df):
    """ Strip categories from dataframe

    >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': ['A', 'B', 'A']})
    >>> df['y'] = df.y.astype('category')
    >>> strip_categories(df)
       x  y
    0  1  0
    1  2  1
    2  3  0
    """
    return pd.DataFrame(dict((col, df[col].cat.codes.values
                                   if iscategorical(df.dtypes[col])
                                   else df[col].values)
                              for col in df.columns),
                        columns=df.columns,
                        index=df.index.codes
                              if iscategorical(df.index.dtype)
                              else df.index)
