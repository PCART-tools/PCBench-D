def percentiles_summary(df, num_old, num_new, upsample=1.0, random_state=None):
    """Summarize data using percentiles and derived weights.

    These summaries can be merged, compressed, and converted back into
    approximate percentiles.

    Parameters
    ----------
    df: pandas.Series
        Data to summarize
    num_old: int
        Number of partitions of the current object
    num_new: int
        Number of partitions of the new object
    upsample: float
        Scale factor to increase the number of percentiles calculated in
        each partition.  Use to improve accuracy.
    """
    from dask.array.percentile import _percentile
    length = len(df)
    if length == 0:
        return ()
    qs = sample_percentiles(num_old, num_new, length, upsample, random_state)
    data = df.values
    interpolation = 'linear'
    if str(data.dtype) == 'category':
        data = data.codes
        interpolation = 'nearest'
    vals = _percentile(data, qs, interpolation=interpolation)
    if interpolation == 'linear' and np.issubdtype(data.dtype, np.integer):
        vals = np.round(vals).astype(data.dtype)
    vals_and_weights = percentiles_to_weights(qs, vals, length)
    return vals_and_weights
