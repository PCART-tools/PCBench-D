def from_dicts(
    data: Sequence[dict[str, Any]],
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
    infer_schema_length: int | None = N_INFER_DEFAULT,
) -> DataFrame:
    """
    Construct a DataFrame from a sequence of dictionaries. This operation clones data.

    Parameters
    ----------
    data
        Sequence with dictionaries mapping column name to value
    schema : Sequence of str, (str,DataType) pairs, or a {str:DataType,} dict
        The DataFrame schema may be declared in several ways:

        * As a dict of {name:type} pairs; if type is None, it will be auto-inferred.
        * As a list of column names; in this case types are automatically inferred.
        * As a list of (name,type) pairs; this is equivalent to the dictionary form.

        If a list of column names is supplied that does NOT match the names in the
        underlying data, the names given here will overwrite the actual fields in
        the order that they appear - however, in this case it is typically clearer
        to rename after loading the frame.

        If you want to drop some of the fields found in the input dictionaries, a
        _partial_ schema can be declared, in which case omitted fields will not be
        loaded. Similarly, you can extend the loaded frame with empty columns by
        adding them to the schema.
    schema_overrides : dict, default None
        Support override of inferred types for one or more columns.
    infer_schema_length
        How many dictionaries/rows to scan to determine the data types
        if set to `None` then ALL dicts are scanned; this will be slow.

    Returns
    -------
    DataFrame

    Examples
    --------
    >>> data = [{"a": 1, "b": 4}, {"a": 2, "b": 5}, {"a": 3, "b": 6}]
    >>> df = pl.from_dicts(data)
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

    Declaring a partial ``schema`` will drop the omitted columns.

    >>> df = pl.from_dicts(data, schema={"a": pl.Int32})
    >>> df
    shape: (3, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ i32 │
    ╞═════╡
    │ 1   │
    │ 2   │
    │ 3   │
    └─────┘

    Can also use the ``schema`` param to extend the loaded columns with one
    or more additional (empty) columns that are not present in the input dicts:

    >>> pl.from_dicts(
    ...     data,
    ...     schema=["a", "b", "c", "d"],
    ...     schema_overrides={"c": pl.Float64, "d": pl.Utf8},
    ... )
    shape: (3, 4)
    ┌─────┬─────┬──────┬──────┐
    │ a   ┆ b   ┆ c    ┆ d    │
    │ --- ┆ --- ┆ ---  ┆ ---  │
    │ i64 ┆ i64 ┆ f64  ┆ str  │
    ╞═════╪═════╪══════╪══════╡
    │ 1   ┆ 4   ┆ null ┆ null │
    │ 2   ┆ 5   ┆ null ┆ null │
    │ 3   ┆ 6   ┆ null ┆ null │
    └─────┴─────┴──────┴──────┘

    """
    if not data and not (schema or schema_overrides):
        raise NoDataError("no data, cannot infer schema")

    return pl.DataFrame(
        data,
        schema=schema,
        schema_overrides=schema_overrides,
        infer_schema_length=infer_schema_length,
    )
