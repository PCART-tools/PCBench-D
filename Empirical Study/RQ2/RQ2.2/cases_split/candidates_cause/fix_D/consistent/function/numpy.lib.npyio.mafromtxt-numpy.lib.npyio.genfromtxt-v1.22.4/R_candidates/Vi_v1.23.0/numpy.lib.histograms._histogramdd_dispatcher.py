def _histogramdd_dispatcher(sample, bins=None, range=None, normed=None,
                            weights=None, density=None):
    if hasattr(sample, 'shape'):  # same condition as used in histogramdd
        yield sample
    else:
        yield from sample
    with contextlib.suppress(TypeError):
        yield from bins
    yield weights
