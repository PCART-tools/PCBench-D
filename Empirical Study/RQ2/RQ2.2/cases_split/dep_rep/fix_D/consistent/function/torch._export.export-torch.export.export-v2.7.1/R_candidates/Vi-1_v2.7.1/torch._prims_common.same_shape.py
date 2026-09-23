def same_shape(a: ShapeType, b: ShapeType, *, allow_rhs_unbacked=False) -> bool:
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    if len(a) != len(b):
        return False

    for x, y in zip(a, b):
        if allow_rhs_unbacked:
            # TODO: We should check that the symbols are consistent
            # with each other
            if isinstance(y, torch.SymInt):
                continue
        # NB: Naively, you would not expect to have to do an oblivious guard
        # here because there is seemingly no broadcasting here, but in fact we
        # use this in some situations to determine if we need to do an expand
        # on the tensor because they don't line up, so you can definitely end
        # up trying to prove u0 != 1 in this situation.  See
        # python test/test_proxy_tensor.py -k test_cumsum_unbacked
        if guard_size_oblivious(x != y):
            return False

    return True
