def partition_to_color(partitions):
    """
    Creates a dictionary with for every item in partition for every partition
    in partitions the index of partition in partitions.

    Parameters
    ----------
    partitions: collections.abc.Sequence[collections.abc.Iterable]
        As returned by :func:`make_partitions`.

    Returns
    -------
    dict
    """
    colors = dict()
    for color, keys in enumerate(partitions):
        for key in keys:
            colors[key] = color
    return colors
