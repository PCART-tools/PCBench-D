@forbid_in_graph
def mark_unbacked(t, index, strict=False):
    """
    Mark a tensor as having an unbacked dim.  This changes the semantics of operations,
    we will always report the size does not equal zero/one, we will turn asserts
    on this index into runtime asserts, and if you try to get the real value we will
    raise an exception.  In other words, we will treat this dimension as if it was
    data dependent (we do not know anything about its value.)

    For historical reasons, by default if an unbacked dim is specialized, we will
    happily specialize it and continue. If you want to error in these cases, pass
    strict=True.
    """
    # You could have copied the mark_dynamic behavior but I'm not convinced
    # it's what you want
    assert not is_traceable_wrapper_subclass(t), "not implemented yet"

    if isinstance(index, int):
        if strict:
            if not hasattr(t, "_dynamo_strict_unbacked_indices"):
                t._dynamo_strict_unbacked_indices = set()
            t._dynamo_strict_unbacked_indices.add(index)
            return

        if not hasattr(t, "_dynamo_unbacked_indices"):
            t._dynamo_unbacked_indices = set()
        t._dynamo_unbacked_indices.add(index)
        return

    assert isinstance(index, (list, tuple))
    for i in index:
        mark_unbacked(t, i)
