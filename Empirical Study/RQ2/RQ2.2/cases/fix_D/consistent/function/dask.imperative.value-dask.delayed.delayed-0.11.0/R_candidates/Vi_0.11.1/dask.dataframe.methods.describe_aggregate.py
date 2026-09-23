def describe_aggregate(values):
    assert len(values) == 6
    count, mean, std, min, q, max = values
    typ = pd.DataFrame if isinstance(count, pd.Series) else pd.Series
    part1 = typ([count, mean, std, min],
                index=['count', 'mean', 'std', 'min'])
    q.index = ['25%', '50%', '75%']
    part3 = typ([max], index=['max'])
    return pd.concat([part1, q, part3])
