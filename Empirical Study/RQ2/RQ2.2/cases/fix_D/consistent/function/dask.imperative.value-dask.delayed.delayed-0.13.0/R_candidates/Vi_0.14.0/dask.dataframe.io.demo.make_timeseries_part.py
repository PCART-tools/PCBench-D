def make_timeseries_part(start, end, dtypes, freq, state_data):
    index = pd.DatetimeIndex(start=start, end=end, freq=freq)
    state = np.random.RandomState(state_data)
    columns = dict((k, make[dt](len(index), state)) for k, dt in dtypes.items())
    df = pd.DataFrame(columns, index=index, columns=sorted(columns))
    if df.index[-1] == end:
        df = df.iloc[:-1]
    return df
