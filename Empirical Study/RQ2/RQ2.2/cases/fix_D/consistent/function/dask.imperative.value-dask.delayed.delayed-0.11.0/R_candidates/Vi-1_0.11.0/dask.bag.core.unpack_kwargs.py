def unpack_kwargs(kwargs):
    """ Extracts dask values from kwargs

    Currently only dask.bag.Item and python literal values are supported.

    Returns a merged dask graph and a list of [key, val] pairs suitable for
    eventually constructing a dict.
    """
    dsk = {}
    kw_pairs = []
    for key, val in iteritems(kwargs):
        if isinstance(val, Item):
            dsk.update(val.dask)
            val = val.key
        # TODO elif isinstance(val, Value):
        elif isinstance(val, Base):
            raise NotImplementedError(
                '%s not supported as kwarg value to Bag.map_partitions'
                % type(val).__name__)
        kw_pairs.append([key, val])
    return dsk, kw_pairs
