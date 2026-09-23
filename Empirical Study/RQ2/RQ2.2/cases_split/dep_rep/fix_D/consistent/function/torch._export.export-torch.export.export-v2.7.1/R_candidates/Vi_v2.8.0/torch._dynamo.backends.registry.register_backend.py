def register_backend(
    compiler_fn: Optional[CompilerFn] = None,
    name: Optional[str] = None,
    tags: Sequence[str] = (),
):
    """
    Decorator to add a given compiler to the registry to allow calling
    `torch.compile` with string shorthand.  Note: for projects not
    imported by default, it might be easier to pass a function directly
    as a backend and not use a string.

    Args:
        compiler_fn: Callable taking a FX graph and fake tensor inputs
        name: Optional name, defaults to `compiler_fn.__name__`
        tags: Optional set of string tags to categorize backend with
    """
    if compiler_fn is None:
        # @register_backend(name="") syntax
        return functools.partial(register_backend, name=name, tags=tags)
    assert callable(compiler_fn)
    name = name or compiler_fn.__name__
    assert name not in _COMPILER_FNS, f"duplicate name: {name}"
    if compiler_fn not in _BACKENDS:
        _BACKENDS[name] = None
    _COMPILER_FNS[name] = compiler_fn
    compiler_fn._tags = tuple(tags)
    return compiler_fn
