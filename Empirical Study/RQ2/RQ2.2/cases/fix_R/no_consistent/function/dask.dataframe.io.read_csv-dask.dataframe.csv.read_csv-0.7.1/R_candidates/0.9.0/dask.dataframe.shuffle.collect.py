def collect(group, p, meta, barrier_token):
    """ Collect partitions from partd, yield dataframes """
    res = p.get(group)
    return res if len(res) > 0 else meta
