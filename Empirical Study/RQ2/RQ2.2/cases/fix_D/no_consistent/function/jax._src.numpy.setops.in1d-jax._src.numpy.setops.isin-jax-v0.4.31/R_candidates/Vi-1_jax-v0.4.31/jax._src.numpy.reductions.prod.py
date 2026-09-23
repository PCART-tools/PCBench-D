def prod(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
         out: None = None, keepdims: bool = False,
         initial: ArrayLike | None = None, where: ArrayLike | None = None,
         promote_integers: bool = True) -> Array:
  r"""Return product of the array elements over a given axis.

  JAX implementation of :func:`numpy.prod`.

  Args:
    a: Input array.
    axis: int or array, default=None. Axis along which the product to be computed.
      If None, the product is computed along all the axes.
    dtype: The type of the output array. Default=None.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    initial: int or array, Default=None. Initial value for the product.
    where: int or array, default=None. The elements to be used in the product.
      Array should be broadcast compatible to the input.
    promote_integers : bool, default=True. If True, then integer inputs will be
      promoted to the widest available integer dtype, following numpy's behavior.
      If False, the result will have the same dtype as the input.
      ``promote_integers`` is ignored if ``dtype`` is specified.
    out: Unused by JAX.

  Returns:
    An array of the product along the given axis.

  See also:
    - :func:`jax.numpy.sum`: Compute the sum of array elements over a given axis.
    - :func:`jax.numpy.max`: Compute the maximum of array elements over given axis.
    - :func:`jax.numpy.min`: Compute the minimum of array elements over given axis.

  Examples:
    By default, ``jnp.prod`` computes along all the axes.

    >>> x = jnp.array([[1, 3, 4, 2],
    ...                [5, 2, 1, 3],
    ...                [2, 1, 3, 1]])
    >>> jnp.prod(x)
    Array(4320, dtype=int32)

    If ``axis=1``, product is computed along axis 1.

    >>> jnp.prod(x, axis=1)
    Array([24, 30,  6], dtype=int32)

    If ``keepdims=True``, ``ndim`` of the output is equal to that of the input.

    >>> jnp.prod(x, axis=1, keepdims=True)
    Array([[24],
           [30],
           [ 6]], dtype=int32)

    To include only specific elements in the sum, you can use a``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.prod(x, axis=1, keepdims=True, where=where)
    Array([[4],
           [3],
           [6]], dtype=int32)
    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.prod(x, axis=1, keepdims=True, where=where)
    Array([[1],
           [1],
           [1]], dtype=int32)
  """
  return _reduce_prod(a, axis=_ensure_optional_axes(axis), dtype=dtype,
                      out=out, keepdims=keepdims, initial=initial, where=where,
                      promote_integers=promote_integers)
