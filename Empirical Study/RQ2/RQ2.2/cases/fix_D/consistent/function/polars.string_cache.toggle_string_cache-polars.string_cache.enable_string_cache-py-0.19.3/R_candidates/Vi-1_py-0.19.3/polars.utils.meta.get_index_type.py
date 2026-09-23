def get_index_type() -> DataTypeClass:
    """
    Get the datatype used for Polars indexing.

    Returns
    -------
    DataType
        :class:`UInt32` in regular Polars, :class:`UInt64` in bigidx Polars.

    """
    return _get_index_type()
