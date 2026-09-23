def static_dispatch_keys(backend: Optional[BackendIndex]) -> List[DispatchKey]:
    if backend is None:
        return []
    else:
        return [
            backend.dispatch_key,
            DispatchKey.CompositeImplicitAutograd,
            DispatchKey.CompositeExplicitAutograd
        ]
