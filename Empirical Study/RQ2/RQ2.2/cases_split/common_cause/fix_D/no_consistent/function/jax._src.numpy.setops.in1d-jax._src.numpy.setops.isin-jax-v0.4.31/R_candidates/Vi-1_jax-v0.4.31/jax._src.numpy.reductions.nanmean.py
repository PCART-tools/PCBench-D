@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanmean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
            keepdims: bool = False, where: ArrayLike | None = None) -> Array:
  r"""Return the mean of the array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanmean`.

  Args:
    a: Input array.
    axis: int or sequence of ints, default=None. Axis along which the mean is
      computed. If None, the mean is computed along the flattened array.
    dtype: The type of the output array. Default=None.
    keepdims: bool, default=False. If True, reduced axes are left in the result
      with size 1.
    where: array of boolean dtype, default=None. The elements to be used in
      computing mean. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array containing the mean of array elements along the given axis, ignoring
    NaNs. If all elements along the given axis are NaNs, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nansum`: Compute the sum of array elements along a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanprod`: Compute the product of array elements along a
      given axis, ignoring NaNs.

  Examples:

    By default, ``jnp.nanmean`` computes the mean of elements along the flattened
    array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[2, nan, 4, 3],
    ...                [nan, -2, nan, 9],
    ...                [4, -7, 6, nan]])
    >>> jnp.nanmean(x)
    Array(2.375, dtype=float32)

    If ``axis=1``, mean will be computed along axis 1.

    >>> jnp.nanmean(x, axis=1)
    Array([3. , 3.5, 1. ], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.nanmean(x, axis=1, keepdims=True)
    Array([[3. ],
           [3.5],
           [1. ]], dtype=float32)

    ``where`` can be used to include only specific elements in computing the mean.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 0, 1, 1],
    ...                    [1, 1, 0, 1]], dtype=bool)
    >>> jnp.nanmean(x, axis=1, keepdims=True, where=where)
    Array([[ 3. ],
           [ 9. ],
           [-1.5]], dtype=float32)

    If ``where`` is ``False`` at all elements, ``jnp.nanmean`` returns ``nan``
    along the given axis.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.nanmean(x, axis=0, keepdims=True, where=where)
    Array([[nan, nan, nan, nan]], dtype=float32)
  """
  check_arraylike("nanmean", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanmean is not supported.")
  if dtypes.issubdtype(dtypes.dtype(a), np.bool_) or dtypes.issubdtype(dtypes.dtype(a), np.integer):
    return mean(a, axis, dtype, out, keepdims, where=where)
  if dtype is None:
    dtype = dtypes.to_inexact_dtype(dtypes.dtype(a, canonicalize=True))
  else:
    dtypes.check_user_dtype_supported(dtype, "mean")
    dtype = dtypes.canonicalize_dtype(dtype)
  nan_mask = lax_internal.bitwise_not(lax_internal._isnan(a))
  normalizer = sum(nan_mask, axis=axis, dtype=dtype, keepdims=keepdims, where=where)
  td = lax.div(nansum(a, axis, dtype=dtype, keepdims=keepdims, where=where), normalizer)
  return td
