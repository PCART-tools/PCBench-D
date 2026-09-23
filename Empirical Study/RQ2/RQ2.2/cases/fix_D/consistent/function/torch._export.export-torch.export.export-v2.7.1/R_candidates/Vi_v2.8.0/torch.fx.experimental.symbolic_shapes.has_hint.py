def has_hint(a: Scalar) -> bool:
    if isinstance(a, SymTypes):
        return a.node.has_hint()
    return True
