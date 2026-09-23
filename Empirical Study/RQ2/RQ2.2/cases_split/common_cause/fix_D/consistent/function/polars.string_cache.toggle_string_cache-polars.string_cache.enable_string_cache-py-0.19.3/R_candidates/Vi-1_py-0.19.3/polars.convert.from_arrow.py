def from_arrow(
    data: (
        pa.Table
        | pa.Array
        | pa.ChunkedArray
        | pa.RecordBatch
        | Iterable[pa.RecordBatch | pa.Table]
    ),
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
    rechunk: bool = True,
) -> DataFrame | Series:
    """
    Create a DataFrame or Series from an Arrow Table or Array.

    This operation will be zero copy for the most part. Types that are not
    supported by Polars may be cast to the closest supported type.

    Parameters
    ----------
    data : :class:`pyarrow.Table`, :class:`pyarrow.Array`, one or more :class:`pyarrow.RecordBatch`
        Data representing an Arrow Table, Array, or sequence of RecordBatches or Tables.
    schema : Sequence of str, (str,DataType) pairs, or a {str:DataType,} dict
        The DataFrame schema may be declared in several ways:

        * As a dict of {name:type} pairs; if type is None, it will be auto-inferred.
        * As a list of column names; in this case types are automatically inferred.
        * As a list of (name,type) pairs; this is equivalent to the dictionary form.

        If you supply a list of column names that does not match the names in the
        underlying data, the names given here will overwrite them. The number
        of names given in the schema should match the underlying data dimensions.
    schema_overrides : dict, default None
        Support type specification or override of one or more columns; note that
        any dtypes inferred from the schema param will be overridden.
    rechunk : bool, default True
        Make sure that all data is in contiguous memory.

    Returns
    -------
    DataFrame or Series

    Examples
    --------
    Constructing a DataFrame from an Arrow Table:

    >>> import pyarrow as pa
    >>> data = pa.table({"a": [1, 2, 3], "b": [4, 5, 6]})
    >>> df = pl.from_arrow(data)
    >>> df
    shape: (3, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 4   │
    │ 2   ┆ 5   │
    │ 3   ┆ 6   │
    └─────┴─────┘

    Constructing a Series from an Arrow Array:

    >>> import pyarrow as pa
    >>> data = pa.array([1, 2, 3])
    >>> series = pl.from_arrow(data, schema={"s": pl.Int32})
    >>> series
    shape: (3,)
    Series: 's' [i32]
    [
        1
        2
        3
    ]

    """  # noqa: W505
    if isinstance(data, pa.Table):
        return pl.DataFrame._from_arrow(
            data=data, rechunk=rechunk, schema=schema, schema_overrides=schema_overrides
        )
    elif isinstance(data, (pa.Array, pa.ChunkedArray)):
        name = getattr(data, "_name", "") or ""
        s = pl.DataFrame(
            data=pl.Series._from_arrow(name, data, rechunk=rechunk),
            schema=schema,
            schema_overrides=schema_overrides,
        ).to_series()
        return s if (name or schema or schema_overrides) else s.alias("")
    elif not data:
        return pl.DataFrame(
            schema=schema,
            schema_overrides=schema_overrides,
        )

    if isinstance(data, pa.RecordBatch):
        data = [data]
    if isinstance(data, Iterable):
        return pl.DataFrame._from_arrow(
            data=pa.Table.from_batches(
                chain.from_iterable(
                    (b.to_batches() if isinstance(b, pa.Table) else [b]) for b in data
                )
            ),
            rechunk=rechunk,
            schema=schema,
            schema_overrides=schema_overrides,
        )

    raise TypeError(
        f"expected PyArrow Table, Array, or one or more RecordBatches; got {type(data).__name__!r}"
    )
