def is_from_source(source: Source, target: Source):
    if isinstance(source, ChainedSource):
        return is_from_source(source.base, target)
    return source == target
