def unzip_namedshape(namedshape):
    if isinstance(namedshape, OrderedDict):
        namedshape = namedshape.items()
    if not hasattr(namedshape, '__iter__') and not isinstance(namedshape, tuple):
        raise RuntimeError(
            'Expected namedshape to be OrderedDict or iterable of tuples, got: {}'
            .format(type(namedshape)))
    if len(namedshape) == 0:
        raise RuntimeError('Expected namedshape to non-empty.')
    return zip(*namedshape)
