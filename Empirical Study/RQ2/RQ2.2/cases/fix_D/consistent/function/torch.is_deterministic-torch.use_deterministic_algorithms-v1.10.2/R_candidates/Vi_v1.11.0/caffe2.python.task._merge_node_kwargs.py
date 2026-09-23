def _merge_node_kwargs(a, b):
    # TODO(azzolini): consistency checks
    if a is None:
        return b
    if b is None:
        return a
    c = copy(a)
    c.update(b)
    return c
