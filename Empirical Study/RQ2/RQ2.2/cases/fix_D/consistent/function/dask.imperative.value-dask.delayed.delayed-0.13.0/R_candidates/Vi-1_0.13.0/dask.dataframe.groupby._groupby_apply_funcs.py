def _groupby_apply_funcs(df, *index, **kwargs):
    """
    Group a dataframe and apply multiple aggregation functions.

    Parameters
    ----------
    df: pandas.DataFrame
        The dataframe to work on.
    index: list of groupers
        If given, they are added to the keyword arguments as the ``by``
        argument.
    funcs: list of result-colum, function, keywordargument triples
        The list of functions that are applied on the grouped data frame.
        Has to be passed as a keyword argument.
    kwargs:
        All keyword arguments, but ``funcs``, are passed verbatim to the groupby
        operation of the dataframe

    Returns
    -------
    aggregated:
        the aggregated dataframe.
    """
    if len(index):
        kwargs.update(by=list(index))

    funcs = kwargs.pop('funcs')
    grouped = df.groupby(**kwargs)

    result = collections.OrderedDict()
    for result_column, func, func_kwargs in funcs:
        result[result_column] = func(grouped, **func_kwargs)

    return pd.DataFrame(result)
