def partition(grouper, sequence, npartitions, p, nelements=2**20):
    """ Partition a bag along a grouper, store partitions on disk """
    for block in partition_all(nelements, sequence):
        d = groupby(grouper, block)
        d2 = defaultdict(list)
        for k, v in d.items():
            d2[abs(hash(k)) % npartitions].extend(v)
        p.append(d2, fsync=True)
    return p
