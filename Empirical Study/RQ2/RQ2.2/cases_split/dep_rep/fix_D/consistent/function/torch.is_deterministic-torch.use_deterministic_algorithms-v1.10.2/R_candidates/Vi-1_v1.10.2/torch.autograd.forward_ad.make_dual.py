def make_dual(tensor, tangent, *, level=None):
    r"""Function that creates a "dual object" that can be used to compute forward AD gradients
    based on the given Tensor and its tangent. It returns a new Tensor that shares memory with
    :attr:`tensor` and the :attr:`tangent` is used as-is.

    This function is backward differentiable.

    Given a function `f` whose jacobian is `J`, it allows to compute the jacobian vector product,
    named `jvp`, between `J` and a given vector `v` as follows.

    Example::
        >>> inp = make_dual(x, v)
        >>> out = f(inp)
        >>> y, jvp = unpack_dual(out)

    """
    if level is None:
        level = _current_level

    if level < 0:
        raise RuntimeError("Trying to create a dual Tensor for forward AD but no level "
                           "exists, make sure to enter_dual_level() first.")

    return torch._VF._make_dual(tensor, tangent, level=level)
