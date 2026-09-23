def from_dict(
    data: Mapping[str, Sequence[object] | Mapping[str, Sequence[object]] | Series],
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame:
    """
    Construct a DataFrame from a dictionary of sequences.

    This operation clones data, unless you pass a ``{str: pl.Series,}`` dict.

    Parameters
    ----------
    data : dict of sequences
        Two-dimensional data represented as a dictionary. dict must contain
        Sequences.
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

    Returns
    -------
    DataFrame

    Examples
    --------
    >>> df = pl.from_dict({"a": [1, 2], "b": [3, 4]})
    >>> df
    shape: (2, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 3   │
    │ 2   ┆ 4   │
    └─────┴─────┘

    """
    return pl.DataFrame._from_dict(
        data, schema=schema, schema_overrides=schema_overrides
    )
