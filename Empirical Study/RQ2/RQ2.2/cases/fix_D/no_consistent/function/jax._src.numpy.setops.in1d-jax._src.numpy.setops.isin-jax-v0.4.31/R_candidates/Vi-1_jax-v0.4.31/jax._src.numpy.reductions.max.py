def max(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None) -> Array:
  r"""Return the maximum of the array elements along a given axis.

  JAX implementation of :func:`numpy.max`.

  Args:
    a: Input array.
    axis: int or array, default=None. Axis along which the maximum to be computed.
      If None, the maximum is computed along all the axes.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    initial: int or array, default=None. Initial value for the maximum.
    where: int or array of boolean dtype, default=None. The elements to be used
      in the maximum. Array should be broadcast compatible to the input.
      ``initial`` must be specified when ``where`` is used.
    out: Unused by JAX.

  Returns:
    An array of maximum values along the given axis.

  See also:
    - :func:`jax.numpy.min`: Compute the minimum of array elements along a given
      axis.
    - :func:`jax.numpy.sum`: Compute the sum of array elements along a given axis.
    - :func:`jax.numpy.prod`: Compute the product of array elements along a given
      axis.

  Examples:

    By default, ``jnp.max`` computes the maximum of elements along all the axes.

    >>> x = jnp.array([[9, 3, 4, 5],
    ...                [5, 2, 7, 4],
    ...                [8, 1, 3, 6]])
    >>> jnp.max(x)
    Array(9, dtype=int32)

    If ``axis=1``, the maximum will be computed along axis 1.

    >>> jnp.max(x, axis=1)
    Array([9, 7, 8], dtype=int32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.max(x, axis=1, keepdims=True)
    Array([[9],
           [7],
           [8]], dtype=int32)

    To include only specific elements in computing the maximum, you can use
    ``where``. It can either have same dimension as input

    >>> where=jnp.array([[0, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.max(x, axis=1, keepdims=True, initial=0, where=where)
    Array([[4],
           [7],
           [8]], dtype=int32)

    or must be broadcast compatible with input.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.max(x, axis=0, keepdims=True, initial=0, where=where)
    Array([[0, 0, 0, 0]], dtype=int32)
  """
  return _reduce_max(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, initial=initial, where=where)
