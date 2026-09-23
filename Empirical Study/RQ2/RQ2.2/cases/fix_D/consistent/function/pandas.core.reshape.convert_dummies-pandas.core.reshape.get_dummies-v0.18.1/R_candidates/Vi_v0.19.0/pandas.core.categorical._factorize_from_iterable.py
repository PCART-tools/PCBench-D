def _factorize_from_iterable(values):
    """
    Factorize an input `values` into `categories` and `codes`. Preserves
    categorical dtype in `categories`.

    *This is an internal function*

    Parameters
    ----------
    values : list-like

    Returns
    -------
    codes : ndarray
    categories : Index
        If `values` has a categorical dtype, then `categories` is
        a CategoricalIndex keeping the categories and order of `values`.
    """
    from pandas.indexes.category import CategoricalIndex

    if not is_list_like(values):
        raise TypeError("Input must be list-like")

    if is_categorical(values):
        if isinstance(values, (ABCCategoricalIndex, ABCSeries)):
            values = values._values
        categories = CategoricalIndex(values.categories,
                                      categories=values.categories,
                                      ordered=values.ordered)
        codes = values.codes
    else:
        cat = Categorical(values, ordered=True)
        categories = cat.categories
        codes = cat.codes
    return codes, categories
