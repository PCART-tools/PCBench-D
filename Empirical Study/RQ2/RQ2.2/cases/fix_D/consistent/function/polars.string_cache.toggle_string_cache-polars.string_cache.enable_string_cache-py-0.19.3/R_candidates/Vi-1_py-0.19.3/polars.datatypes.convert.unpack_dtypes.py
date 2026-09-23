def unpack_dtypes(
    *dtypes: PolarsDataType | None,
    include_compound: bool = False,
) -> set[PolarsDataType]:
    """
    Return a set of unique dtypes found in one or more (potentially compound) dtypes.

    Parameters
    ----------
    *dtypes
        One or more Polars dtypes.
    include_compound
        * if True, any parent/compound dtypes (List, Struct) are included in the result.
        * if False, only the child/scalar dtypes are returned from these types.

    Examples
    --------
    >>> from polars.datatypes import unpack_dtypes
    >>> list_dtype = [pl.List(pl.Float64)]
    >>> struct_dtype = pl.Struct(
    ...     [
    ...         pl.Field("a", pl.Int64),
    ...         pl.Field("b", pl.Utf8),
    ...         pl.Field("c", pl.List(pl.Float64)),
    ...     ]
    ... )
    >>> unpack_dtypes([struct_dtype, list_dtype])  # doctest: +IGNORE_RESULT
    {Float64, Int64, Utf8}
    >>> unpack_dtypes(
    ...     [struct_dtype, list_dtype], include_compound=True
    ... )  # doctest: +IGNORE_RESULT
    {Float64, Int64, Utf8, List(Float64), Struct([Field('a', Int64), Field('b', Utf8), Field('c', List(Float64))])}

    """  # noqa: W505
    if not dtypes:
        return set()
    elif len(dtypes) == 1 and isinstance(dtypes[0], Collection):
        dtypes = dtypes[0]

    unpacked: set[PolarsDataType] = set()
    for tp in dtypes:
        if isinstance(tp, List):
            if include_compound:
                unpacked.add(tp)
            unpacked.update(unpack_dtypes(tp.inner, include_compound=include_compound))
        elif isinstance(tp, Struct):
            if include_compound:
                unpacked.add(tp)
            unpacked.update(unpack_dtypes(tp.fields, include_compound=include_compound))  # type: ignore[arg-type]
        elif isinstance(tp, Field):
            unpacked.update(unpack_dtypes(tp.dtype, include_compound=include_compound))
        elif tp is not None and is_polars_dtype(tp):
            unpacked.add(tp)
    return unpacked
