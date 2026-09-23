def from_numpy(
    data: np.ndarray[Any, Any],
    schema: SchemaDefinition | None = None,
    *,
    schema_overrides: SchemaDict | None = None,
    orient: Orientation | None = None,
) -> DataFrame:
    """
    Construct a DataFrame from a numpy ndarray. This operation clones data.

    Note that this is slower than creating from columnar memory.

    Parameters
    ----------
    data : :class:`numpy.ndarray`
        Two-dimensional data represented as a numpy ndarray.
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

    Returns
    -------
    DataFrame

    Examples
    --------
    >>> import numpy as np
    >>> data = np.array([[1, 2, 3], [4, 5, 6]])
    >>> df = pl.from_numpy(data, schema=["a", "b"], orient="col")
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
    return pl.DataFrame._from_numpy(
        data, schema=schema, orient=orient, schema_overrides=schema_overrides
    )
