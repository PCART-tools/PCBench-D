def from_records(
    data: Sequence[Any],
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
    orient: Orientation | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
) -> DataFrame:
    """
    Construct a DataFrame from a sequence of sequences. This operation clones data.

    Note that this is slower than creating from columnar memory.

    Parameters
    ----------
    data : Sequence of sequences
        Two-dimensional data represented as a sequence of sequences.
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
        any dtypes inferred from the columns param will be overridden.
    orient : {None, 'col', 'row'}
        Whether to interpret two-dimensional data as columns or as rows. If None,
        the orientation is inferred by matching the columns and data dimensions. If
        this does not yield conclusive results, column orientation is used.
    infer_schema_length
        How many dictionaries/rows to scan to determine the data types
        if set to `None` all rows are scanned. This will be slow.

    Returns
    -------
    DataFrame

    Examples
    --------
    >>> data = [[1, 2, 3], [4, 5, 6]]
    >>> df = pl.from_records(data, schema=["a", "b"])
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

    """
    return pl.DataFrame._from_records(
        data,
        schema=schema,
        schema_overrides=schema_overrides,
        orient=orient,
        infer_schema_length=infer_schema_length,
    )
