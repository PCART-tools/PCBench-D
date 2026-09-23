@functools.lru_cache
def is_from_unspecialized_builtin_nn_module_source(source: Source):
    if isinstance(source, UnspecializedBuiltinNNModuleSource):
        return True
    if isinstance(source, ChainedSource):
        return is_from_unspecialized_builtin_nn_module_source(source.base)
    return False
