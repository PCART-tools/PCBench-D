def ptp(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False) -> Array:
  r"""Return the peak-to-peak range along a given axis.

  JAX implementation of :func:`numpy.ptp`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      range is computed. If None, the range is computed on the flattened array.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    out: Unused by JAX.

  Returns:
    An array with the range of elements along specified axis of input.

  Examples:
    By default, ``jnp.ptp`` computes the range along all axes.

    >>> x = jnp.array([[1, 3, 5, 2],
    ...                [4, 6, 8, 1],
    ...                [7, 9, 3, 4]])
    >>> jnp.ptp(x)
    Array(8, dtype=int32)

    If ``axis=1``, computes the range along axis 1.

    >>> jnp.ptp(x, axis=1)
    Array([4, 7, 6], dtype=int32)

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> jnp.ptp(x, axis=1, keepdims=True)
    Array([[4],
           [7],
           [6]], dtype=int32)
  """
  return _ptp(a, _ensure_optional_axes(axis), out, keepdims)
