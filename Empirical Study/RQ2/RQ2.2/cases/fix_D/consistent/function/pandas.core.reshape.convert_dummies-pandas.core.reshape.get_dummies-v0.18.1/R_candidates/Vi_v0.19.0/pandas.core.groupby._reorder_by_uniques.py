def _reorder_by_uniques(uniques, labels):
    # sorter is index where elements ought to go
    sorter = uniques.argsort()

    # reverse_indexer is where elements came from
    reverse_indexer = np.empty(len(sorter), dtype=np.int64)
    reverse_indexer.put(sorter, np.arange(len(sorter)))

    mask = labels < 0

    # move labels to right locations (ie, unsort ascending labels)
    labels = algos.take_nd(reverse_indexer, labels, allow_fill=False)
    np.putmask(labels, mask, -1)

    # sort observed ids
    uniques = algos.take_nd(uniques, sorter, allow_fill=False)

    return uniques, labels
