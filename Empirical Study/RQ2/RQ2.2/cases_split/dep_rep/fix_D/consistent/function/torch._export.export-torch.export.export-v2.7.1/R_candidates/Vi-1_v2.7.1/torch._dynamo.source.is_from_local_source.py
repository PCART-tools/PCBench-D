def is_from_local_source(source: Source, *, only_allow_input=False):
    if isinstance(source, ChainedSource):
        return is_from_local_source(source.base, only_allow_input=only_allow_input)
    if not isinstance(source, LocalSource):
        return False
    if only_allow_input and not source.is_input:
        return False
    return True
