def is_observed_standalone_module(module: Any) -> bool:
    return isinstance(module, ObservedStandaloneGraphModule)
