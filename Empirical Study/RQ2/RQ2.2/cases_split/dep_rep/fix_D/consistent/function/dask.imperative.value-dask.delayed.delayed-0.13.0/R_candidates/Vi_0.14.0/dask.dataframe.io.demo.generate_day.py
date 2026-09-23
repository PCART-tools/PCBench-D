def generate_day(date, open, high, low, close, volume,
                 freq=pd.Timedelta(seconds=60), random_state=None):
    """ Generate a day of financial data from open/close high/low values """
    if not isinstance(random_state, np.random.RandomState):
        random_state = np.random.RandomState(random_state)
    if not isinstance(date, pd.Timestamp):
        date = pd.Timestamp(date)
    if not isinstance(freq, pd.Timedelta):
        freq = pd.Timedelta(freq)

    time = pd.date_range(date + pd.Timedelta(hours=9),
                         date + pd.Timedelta(hours=12 + 4),
                         freq=freq / 5, name='timestamp')
    n = len(time)
    while True:
        values = (random_state.random_sample(n) - 0.5).cumsum()
        values *= (high - low) / (values.max() - values.min())  # scale
        values += np.linspace(open - values[0], close - values[-1],
                              len(values))  # endpoints
        assert np.allclose(open, values[0])
        assert np.allclose(close, values[-1])

        mx = max(close, open)
        mn = min(close, open)
        ind = values > mx
        values[ind] = (values[ind] - mx) * (high - mx) / (values.max() - mx) + mx
        ind = values < mn
        values[ind] = (values[ind] - mn) * (low - mn) / (values.min() - mn) + mn
        # The process fails if min/max are the same as open close.  This is rare
        if (np.allclose(values.max(), high) and np.allclose(values.min(), low)):
            break

    s = pd.Series(values.round(3), index=time)
    rs = s.resample(freq)
    # TODO: add in volume
    return pd.DataFrame({'open': rs.first(),
                         'close': rs.last(),
                         'high': rs.max(),
                         'low': rs.min()})
