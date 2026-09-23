def _get_layout(name):
    """Get layout extension object from its string representation.
    """
    cache = _get_layout.cache   # type: ignore[attr-defined]
    if not cache:
        for v in torch.__dict__.values():
            if isinstance(v, torch.layout):
                cache[str(v)] = v
    return cache[name]
