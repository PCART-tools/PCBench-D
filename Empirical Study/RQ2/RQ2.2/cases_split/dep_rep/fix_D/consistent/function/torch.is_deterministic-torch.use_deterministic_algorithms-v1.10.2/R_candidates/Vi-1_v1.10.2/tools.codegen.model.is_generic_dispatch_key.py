def is_generic_dispatch_key(dk: DispatchKey) -> bool:
    return dk in {DispatchKey.CompositeExplicitAutograd, DispatchKey.CompositeImplicitAutograd}
