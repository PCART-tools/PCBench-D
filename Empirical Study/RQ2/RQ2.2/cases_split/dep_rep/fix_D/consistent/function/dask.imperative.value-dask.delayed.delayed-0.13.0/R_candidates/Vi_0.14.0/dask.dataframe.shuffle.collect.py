def collect(p, part, meta, barrier_token):
    """ Collect partitions from partd, yield dataframes """
    res = p.get(part)
    return res if len(res) > 0 else meta
