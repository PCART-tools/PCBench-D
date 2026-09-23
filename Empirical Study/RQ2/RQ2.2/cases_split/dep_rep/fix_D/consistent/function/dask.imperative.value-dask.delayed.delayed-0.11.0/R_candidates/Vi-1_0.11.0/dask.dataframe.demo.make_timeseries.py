def make_timeseries(start, end, dtypes, freq, partition_freq, seed=None):
    """ Create timeseries dataframe with random data

    Parameters
    ----------
    start: datetime (or datetime-like string)
        Start of time series
    end: datetime (or datetime-like string)
        End of time series
    dtypes: dict
        Mapping of column names to types.
        Valid types include {float, int, str, 'category'}
    freq: string
        String like '2s' or '1H' or '12W' for the time series frequency
    partition_freq: string
        String like '1M' or '2Y' to divide the dataframe into partitions
    seed: int (optional)
        Randomstate seed

    >>> import dask.dataframe as dd
    >>> df = dd.demo.make_timeseries('2000', '2010',
    ...                              {'value': float, 'name': str, 'id': int},
    ...                              freq='2H', partition_freq='1D', seed=1)
    >>> df.head()
                           id    name     value
    2000-01-01 00:00:00   960     Dan  0.824008
    2000-01-01 02:00:00  1033  Xavier  0.575390
    2000-01-01 04:00:00   986  George  0.693842
    2000-01-01 06:00:00  1073   Sarah  0.900580
    2000-01-01 08:00:00   976  Hannah -0.373847
    """
    divisions = list(pd.DatetimeIndex(start=start, end=end,
                                      freq=partition_freq))
    state = np.random.RandomState(seed)
    seeds = different_seeds(len(divisions), state)
    name = 'make-timeseries-' + tokenize(start, end, dtypes, freq, partition_freq)
    dsk = dict(((name, i), (make_timeseries_part, divisions[i], divisions[i + 1],
                                                 dtypes, freq, seeds[i]))
                for i in range(len(divisions) - 1))
    head = make_timeseries_part('2000', '2000', dtypes, '1H', 1)
    return DataFrame(dsk, name, head, divisions)
