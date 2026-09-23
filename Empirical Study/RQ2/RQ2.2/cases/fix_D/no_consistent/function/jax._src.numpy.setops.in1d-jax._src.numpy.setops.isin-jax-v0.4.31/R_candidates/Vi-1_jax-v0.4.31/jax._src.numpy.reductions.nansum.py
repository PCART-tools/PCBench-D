@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nansum(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
           keepdims: bool = False, initial: ArrayLike | None = None,
           where: ArrayLike | None = None) -> Array:
  r"""Return the sum of the array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nansum`.

  Args:
    a: Input array.
    axis: int or sequence of ints, default=None. Axis along which the sum is
      computed. If None, the sum is computed along the flattened array.
    dtype: The type of the output array. Default=None.
    keepdims: bool, default=False. If True, reduced axes are left in the result
      with size 1.
    initial: int or array, default=None. Initial value for the sum.
    where: array of boolean dtype, default=None. The elements to be used in the
      sum. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array containing the sum of array elements along the given axis, ignoring
    NaNs. If all elements along the given axis are NaNs, returns 0.

  See also:
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanprod`: Compute the product of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements along a given
      axis, ignoring NaNs.

  Examples:

    By default, ``jnp.nansum`` computes the sum of elements along the flattened
    array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[3, nan, 4, 5],
    ...                [nan, -2, nan, 7],
    ...                [2, 1, 6, nan]])
    >>> jnp.nansum(x)
    Array(26., dtype=float32)

    If ``axis=1``, the sum will be computed along axis 1.

    >>> jnp.nansum(x, axis=1)
    Array([12.,  5.,  9.], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.nansum(x, axis=1, keepdims=True)
    Array([[12.],
           [ 5.],
           [ 9.]], dtype=float32)

    To include only specific elements in computing the sum, you can use ``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.nansum(x, axis=1, keepdims=True, where=where)
    Array([[7.],
           [7.],
           [9.]], dtype=float32)

    If ``where`` is ``False`` at all elements, ``jnp.nansum`` returns 0 along
    the given axis.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.nansum(x, axis=0, keepdims=True, where=where)
    Array([[0., 0., 0., 0.]], dtype=float32)
  """
  dtypes.check_user_dtype_supported(dtype, "nanprod")
  return _nan_reduction(a, 'nansum', sum, 0, nan_if_all_nan=False,
                        axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        initial=initial, where=where)
