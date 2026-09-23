def _check_for_unsupported_types(dtypes: list[PolarsDataType]) -> None:
    schema_dtypes = unpack_dtypes(*dtypes)
    unsupported_types = {Time, Categorical, Null}
    overlap = schema_dtypes & unsupported_types

    if overlap:
        raise TypeError(f"dataframe contains unsupported data types: {overlap!r}")
