@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanprod(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
            keepdims: bool = False, initial: ArrayLike | None = None,
            where: ArrayLike | None = None) -> Array:
  r"""Return the product of the array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanprod`.

  Args:
    a: Input array.
    axis: int or sequence of ints, default=None. Axis along which the product is
      computed. If None, the product is computed along the flattened array.
    dtype: The type of the output array. Default=None.
    keepdims: bool, default=False. If True, reduced axes are left in the result
      with size 1.
    initial: int or array, default=None. Initial value for the product.
    where: array of boolean dtype, default=None. The elements to be used in the
      product. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array containing the product of array elements along the given axis,
    ignoring NaNs. If all elements along the given axis are NaNs, returns 1.

  See also:
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nansum`: Compute the sum of array elements along a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements along a given
      axis, ignoring NaNs.

  Examples:

    By default, ``jnp.nanprod`` computes the product of elements along the flattened
    array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[nan, 3, 4, nan],
    ...                [5, nan, 1, 3],
    ...                [2, 1, nan, 1]])
    >>> jnp.nanprod(x)
    Array(360., dtype=float32)

    If ``axis=1``, the product will be computed along axis 1.

    >>> jnp.nanprod(x, axis=1)
    Array([12., 15.,  2.], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.nanprod(x, axis=1, keepdims=True)
    Array([[12.],
           [15.],
           [ 2.]], dtype=float32)

    To include only specific elements in computing the maximum, you can use ``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.nanprod(x, axis=1, keepdims=True, where=where)
    Array([[4.],
           [3.],
           [2.]], dtype=float32)

    If ``where`` is ``False`` at all elements, ``jnp.nanprod`` returns 1 along
    the given axis.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.nanprod(x, axis=0, keepdims=True, where=where)
    Array([[1., 1., 1., 1.]], dtype=float32)
  """
  dtypes.check_user_dtype_supported(dtype, "nanprod")
  return _nan_reduction(a, 'nanprod', prod, 1, nan_if_all_nan=False,
                        axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        initial=initial, where=where)
