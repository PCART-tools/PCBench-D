@functools.lru_cache
def is_from_unspecialized_nn_module_source(source: Source):
    if isinstance(source, UnspecializedNNModuleSource):
        return True
    if isinstance(source, ChainedSource):
        return is_from_unspecialized_nn_module_source(source.base)
    return False
