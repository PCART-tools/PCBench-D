@deprecate_nonkeyword_arguments(allowed_args=["inner_dtype"], version="0.19.3")
def create_list_strategy(
    inner_dtype: PolarsDataType | None,
    select_from: Sequence[Any] | None = None,
    size: int | None = None,
    min_size: int | None = None,
    max_size: int | None = None,
    unique: bool = False,  # noqa: FBT001
) -> SearchStrategy[list[Any]]:
    """
    Hypothesis strategy for producing polars List data.

    Parameters
    ----------
    inner_dtype : PolarsDataType
        type of the inner list elements (can also be another List).
    select_from : list, optional
        randomly select the innermost values from this list (otherwise
        the default strategy associated with the innermost dtype is used).
    size : int, optional
        if set, generated lists will be of exactly this size (and
        ignore the min_size/max_size params).
    min_size : int, optional
        set the minimum size of the generated lists (default: 0 if unset).
    max_size : int, optional
        set the maximum size of the generated lists (default: 3 if
        min_size is unset or zero, otherwise 2x min_size).
    unique : bool, optional
        ensure that the generated lists contain unique values.

    Examples
    --------
    Create a strategy that generates a list of i32 values:

    >>> lst = create_list_strategy(inner_dtype=pl.Int32)
    >>> lst.example()  # doctest: +SKIP
    [-11330, 24030, 116]

    Create a strategy that generates lists of lists of specific strings:

    >>> lst = create_list_strategy(
    ...     inner_dtype=pl.List(pl.Utf8),
    ...     select_from=["xx", "yy", "zz"],
    ... )
    >>> lst.example()  # doctest: +SKIP
    [['yy', 'xx'], [], ['zz']]

    Create a UInt8 dtype strategy as a hypothesis composite that generates
    pairs of small int values where the first is always <= the second:

    >>> from hypothesis.strategies import composite
    >>>
    >>> @composite
    ... def uint8_pairs(draw, uints=create_list_strategy(pl.UInt8, size=2)):
    ...     pairs = list(zip(draw(uints), draw(uints)))
    ...     return [sorted(ints) for ints in pairs]
    ...
    >>> uint8_pairs().example()  # doctest: +SKIP
    [(12, 22), (15, 131)]
    >>> uint8_pairs().example()  # doctest: +SKIP
    [(59, 176), (149, 149)]

    """
    if select_from and inner_dtype is None:
        raise ValueError("if specifying `select_from`, must also specify `inner_dtype`")

    if inner_dtype is None:
        strats = list(
            # note: remove the restriction on nested Categoricals after
            # https://github.com/pola-rs/polars/issues/8563 is fixed
            _get_strategy_dtypes(
                base_type=True,
                excluding=Categorical,
            )
        )
        shuffle(strats)
        inner_dtype = choice(strats)
    if size:
        min_size = max_size = size
    else:
        min_size = min_size or 0
        if max_size is None:
            max_size = 3 if not min_size else (min_size * 2)

    if inner_dtype == List:
        st = create_list_strategy(
            inner_dtype=inner_dtype.inner,  # type: ignore[union-attr]
            select_from=select_from,
            min_size=min_size,
            max_size=max_size,
        )
        if inner_dtype.inner is None and hasattr(st, "_dtype"):  # type: ignore[union-attr]
            inner_dtype = st._dtype
    else:
        st = (
            sampled_from(list(select_from))
            if select_from
            else scalar_strategies[inner_dtype]
        )

    ls = lists(
        elements=st,
        min_size=min_size,
        max_size=max_size,
        unique_by=(_flexhash if unique else None),
    )
    ls._dtype = List(inner_dtype)  # type: ignore[attr-defined, arg-type]
    return ls
