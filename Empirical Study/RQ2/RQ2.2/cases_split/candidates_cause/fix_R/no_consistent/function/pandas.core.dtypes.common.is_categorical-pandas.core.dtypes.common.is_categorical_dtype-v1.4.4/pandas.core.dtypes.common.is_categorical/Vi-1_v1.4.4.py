def is_categorical(arr) -> bool:
    """
    Check whether an array-like is a Categorical instance.

    Parameters
    ----------
    arr : array-like
        The array-like to check.

    Returns
    -------
    boolean
        Whether or not the array-like is of a Categorical instance.

    Examples
    --------
    >>> is_categorical([1, 2, 3])
    False

    Categoricals, Series Categoricals, and CategoricalIndex will return True.

    >>> cat = pd.Categorical([1, 2, 3])
    >>> is_categorical(cat)
    True
    >>> is_categorical(pd.Series(cat))
    True
    >>> is_categorical(pd.CategoricalIndex([1, 2, 3]))
    True
    """
    warnings.warn(
        "is_categorical is deprecated and will be removed in a future version. "
        "Use is_categorical_dtype instead.",
        FutureWarning,
        stacklevel=find_stack_level(),
    )
    return isinstance(arr, ABCCategorical) or is_categorical_dtype(arr)
