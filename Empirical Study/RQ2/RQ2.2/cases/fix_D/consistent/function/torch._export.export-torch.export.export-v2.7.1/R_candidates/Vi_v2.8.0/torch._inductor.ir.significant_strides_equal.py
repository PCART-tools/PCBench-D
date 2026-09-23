def significant_strides_equal(
    strides1: Sequence[_IntLike],
    strides2: Sequence[_IntLike],
    shape: Sequence[_IntLike],
) -> bool:
    """
    Returns true if the strides are equal, ignoring dimensions of size 1 .
    """
    assert len(shape) == len(strides1) and len(strides1) == len(strides2)
    for dim, s1, s2 in zip(shape, strides1, strides2):
        if V.graph.sizevars.statically_known_leq(dim, 1):  # type: ignore[arg-type]
            continue

        if not V.graph.sizevars.statically_known_equals(
            s1, s2
        ) and not V.graph.sizevars.symbolic_hint(s1) == V.graph.sizevars.symbolic_hint(
            s2
        ):
            return False

    return True
