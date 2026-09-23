def _get_spec(func: FunctionType) -> FunctionSpec:
    spec = _spec_cache.get(func)
    if spec is None:
        spec = FunctionSpec(func)
        _spec_cache[func] = spec
    return spec
