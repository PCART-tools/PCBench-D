def _scan_pyarrow_dataset(
    ds: pa.dataset.Dataset,
    *,
    allow_pyarrow_filter: bool = True,
    batch_size: int | None = None,
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
    batch_size
        The maximum row count for scanned pyarrow record batches.

    """
    func = partial(_scan_pyarrow_dataset_impl, ds, batch_size=batch_size)
    return pl.LazyFrame._scan_python_function(
        ds.schema, func, pyarrow=allow_pyarrow_filter
    )
