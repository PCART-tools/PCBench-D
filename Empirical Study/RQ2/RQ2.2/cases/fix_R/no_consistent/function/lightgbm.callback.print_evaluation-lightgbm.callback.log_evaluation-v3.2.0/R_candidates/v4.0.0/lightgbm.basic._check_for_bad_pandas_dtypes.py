def _check_for_bad_pandas_dtypes(pandas_dtypes_series: pd_Series) -> None:
    bad_pandas_dtypes = [
        f'{column_name}: {pandas_dtype}'
        for column_name, pandas_dtype in pandas_dtypes_series.items()
        if not _is_allowed_numpy_dtype(pandas_dtype.type)
    ]
    if bad_pandas_dtypes:
        raise ValueError('pandas dtypes must be int, float or bool.\n'
                         f'Fields with bad pandas dtypes: {", ".join(bad_pandas_dtypes)}')
