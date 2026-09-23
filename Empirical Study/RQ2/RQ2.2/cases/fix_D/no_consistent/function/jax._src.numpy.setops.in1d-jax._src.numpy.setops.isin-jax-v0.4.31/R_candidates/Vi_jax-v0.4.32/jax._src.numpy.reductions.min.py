def min(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None) -> Array:
  r"""Return the minimum of array elements along a given axis.

  JAX implementation of :func:`numpy.min`.

  Args:
    a: Input array.
    axis: int or array, default=None. Axis along which the minimum to be computed.
      If None, the minimum is computed along all the axes.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    initial: int or array, Default=None. Initial value for the minimum.
    where: int or array, default=None. The elements to be used in the minimum.
      Array should be broadcast compatible to the input. ``initial`` must be
      specified when ``where`` is used.
    out: Unused by JAX.

  Returns:
    An array of minimum values along the given axis.

  See also:
    - :func:`jax.numpy.max`: Compute the maximum of array elements along a given
      axis.
    - :func:`jax.numpy.sum`: Compute the sum of array elements along a given axis.
    - :func:`jax.numpy.prod`: Compute the product of array elements along a given
      axis.

  Examples:
    By default, the minimum is computed along all the axes.

    >>> x = jnp.array([[2, 5, 1, 6],
    ...                [3, -7, -2, 4],
    ...                [8, -4, 1, -3]])
    >>> jnp.min(x)
    Array(-7, dtype=int32)

    If ``axis=1``, the minimum is computed along axis 1.

    >>> jnp.min(x, axis=1)
    Array([ 1, -7, -4], dtype=int32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.min(x, axis=1, keepdims=True)
    Array([[ 1],
           [-7],
           [-4]], dtype=int32)

    To include only specific elements in computing the minimum, you can use
    ``where``. ``where`` can either have same dimension as input.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.min(x, axis=1, keepdims=True, initial=0, where=where)
    Array([[ 0],
           [-2],
           [-4]], dtype=int32)

    or must be broadcast compatible with input.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.min(x, axis=0, keepdims=True, initial=0, where=where)
    Array([[0, 0, 0, 0]], dtype=int32)
  """
  return _reduce_min(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, initial=initial, where=where)
