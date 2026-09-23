def list_backends(exclude_tags=("debug", "experimental")) -> list[str]:
    """
    Return valid strings that can be passed to:

        torch.compile(..., backend="name")
    """
    _lazy_import()
    exclude_tags = set(exclude_tags or ())

    backends = [
        name
        for name in _BACKENDS.keys()
        if name not in _COMPILER_FNS
        or not exclude_tags.intersection(_COMPILER_FNS[name]._tags)
    ]
    return sorted(backends)
