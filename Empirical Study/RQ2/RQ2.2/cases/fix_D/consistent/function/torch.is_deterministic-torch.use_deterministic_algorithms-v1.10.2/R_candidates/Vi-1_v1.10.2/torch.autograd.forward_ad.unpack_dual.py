def unpack_dual(tensor, *, level=None):
    r"""Function that unpacks a "dual object" to recover two plain tensors, one representing
    the primal and the other the tangent (both are views of :attr:`tensor`. Neither of these
    tensors can be dual tensor of level :attr:`level`.

    This function is backward differentiable.
    """
    if level is None:
        level = _current_level

    if level < 0:
        return tensor, None

    return torch._VF._unpack_dual(tensor, level=level)
