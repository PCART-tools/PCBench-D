def make_dual(tensor, tangent, *, level=None):
    r"""Associates a tensor value with a forward gradient, the tangent, to create a
    "dual tensor", which is used to compute forward AD gradients.
    The result is a new tensor aliased to :attr:`tensor` with :attr:`tangent` embedded
    as an attribute as-is if it has the same storage layout or copied otherwise.
    The tangent attribute can be recovered with :func:`unpack_dual`.

    This function is backward differentiable.

    Given a function `f` whose jacobian is `J`, it allows one to compute the Jacobian-vector product (`jvp`)
    between `J` and a given vector `v` as follows.

    Example::

        >>> with dual_level():
        ...   inp = make_dual(x, v)
        ...   out = f(inp)
        ...   y, jvp = unpack_dual(out)

    Please see the `forward-mode AD tutorial <https://pytorch.org/tutorials/intermediate/forward_ad_usage.html>`__
    for detailed steps on how to use this API.

    """
    if level is None:
        level = _current_level

    if level < 0:
        raise RuntimeError("Trying to create a dual Tensor for forward AD but no level "
                           "exists, make sure to enter_dual_level() first.")

    return torch._VF._make_dual(tensor, tangent, level=level)
