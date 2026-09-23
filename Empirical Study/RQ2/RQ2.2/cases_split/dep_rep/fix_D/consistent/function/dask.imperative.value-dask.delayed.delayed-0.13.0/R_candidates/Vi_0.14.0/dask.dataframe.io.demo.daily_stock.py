def daily_stock(symbol, start, stop, freq=pd.Timedelta(seconds=1),
                data_source='yahoo', random_state=None):
    """ Create artificial stock data

    This data matches daily open/high/low/close values from Yahoo! Finance, but
    interpolates values within each day with random values.  This makes the
    results look natural without requiring the downloading of large volumes of
    data.  This is useful for education and benchmarking.

    Parameters
    ----------
    symbol: string
        A stock symbol like "GOOG" or "F"
    start: date, str, or pd.Timestamp
        The start date, input will be fed into pd.Timestamp for normalization
    stop: date, str, or pd.Timestamp
        The start date, input will be fed into pd.Timestamp for normalization
    freq: timedelta, str, or pd.Timedelta
        The frequency of sampling
    data_source: str, optional
        defaults to 'yahoo'.  See pandas_datareader.data.DataReader for options
    random_state: int, np.random.RandomState object
        random seed, defaults to randomly chosen

    Examples
    --------
    >>> import dask.dataframe as dd
    >>> df = dd.demo.daily_stock('GOOG', '2010', '2011', freq='1s')
    >>> df  # doctest: +NORMALIZE_WHITESPACE
    Dask DataFrame Structure:
                           close     high      low     open
    npartitions=252
    2010-01-04 09:00:00  float64  float64  float64  float64
    2010-01-05 09:00:00      ...      ...      ...      ...
    ...                      ...      ...      ...      ...
    2010-12-31 09:00:00      ...      ...      ...      ...
    2010-12-31 16:00:00      ...      ...      ...      ...
    Dask Name: from-delayed, 504 tasks

    >>> df.head()  # doctest: +SKIP
                           close     high      low     open
    timestamp
    2010-01-04 09:00:00  626.944  626.964  626.944  626.951
    2010-01-04 09:00:01  626.906  626.931  626.906  626.931
    2010-01-04 09:00:02  626.901  626.911  626.901  626.905
    2010-01-04 09:00:03  626.920  626.920  626.905  626.905
    2010-01-04 09:00:04  626.894  626.917  626.894  626.906
    """
    from pandas_datareader import data
    df = data.DataReader(symbol, data_source, start, stop)
    seeds = random_state_data(len(df), random_state=random_state)
    parts = []
    divisions = []
    for i, seed in zip(range(len(df)), seeds):
        s = df.iloc[i]
        part = delayed(generate_day)(s.name, s.loc['Open'], s.loc['High'], s.loc['Low'],
                                     s.loc['Close'], s.loc['Volume'],
                                     freq=freq, random_state=seeds)
        parts.append(part)
        divisions.append(s.name + pd.Timedelta(hours=9))

    divisions.append(s.name + pd.Timedelta(hours=12 + 4))

    meta = generate_day('2000-01-01', 1, 2, 0, 1, 100)

    return from_delayed(parts, meta=meta, divisions=divisions)
