def collect(grouper, group, p, barrier_token):
    """ Collect partitions from disk and yield k,v group pairs """
    d = groupby(grouper, p.get(group, lock=False))
    return list(d.items())
