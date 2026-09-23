def _scan_pyarrow_dataset(
    ds: pa.dataset.Dataset, allow_pyarrow_filter: bool = True
) -> LazyFrame:
    """
    Pickle the partially applied function `_scan_pyarrow_dataset_impl`.

    The bytes are then sent to the polars logical plan. It can be deserialized once
    executed and ran.

    Parameters
    ----------
    ds
        pyarrow dataset
    allow_pyarrow_filter
        Allow predicates to be pushed down to pyarrow. This can lead to different
        results if comparisons are done with null values as pyarrow handles this
        different than polars does.

    """
    func = partial(_scan_pyarrow_dataset_impl, ds)
    func_serialized = pickle.dumps(func)
    return pli.LazyFrame._scan_python_function(
        ds.schema, func_serialized, allow_pyarrow_filter
    )
