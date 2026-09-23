@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanvar(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
           ddof: int = 0, keepdims: bool = False,
           where: ArrayLike | None = None) -> Array:
  r"""Compute the variance of array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanvar`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      variance is computed. If None, variance is computed along flattened array.
    dtype: The type of the output array. Default=None.
    ddof: int, default=0. Degrees of freedom. The divisor in the variance computation
      is ``N-ddof``, ``N`` is number of elements along given axis.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      variance. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array containing the variance of array elements along specified axis. If
    all elements along the given axis are NaNs, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements over a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanstd`: Computed the standard deviation of a given axis,
      ignoring NaNs.
    - :func:`jax.numpy.var`: Compute the variance of array elements along a given
      axis.

  Examples:
    By default, ``jnp.nanvar`` computes the variance along all axes.

    >>> nan = jnp.nan
    >>> x = jnp.array([[1, nan, 4, 3],
    ...                [nan, 2, nan, 9],
    ...                [4, 8, 6, nan]])
    >>> jnp.nanvar(x)
    Array(6.984375, dtype=float32)

    If ``axis=1``, variance is computed along axis 1.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.nanvar(x, axis=1))
    [ 1.56 12.25  2.67]

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.nanvar(x, axis=1, keepdims=True))
    [[ 1.56]
     [12.25]
     [ 2.67]]

    If ``ddof=1``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.nanvar(x, axis=1, keepdims=True, ddof=1))
    [[ 2.33]
     [24.5 ]
     [ 4.  ]]

    To include specific elements of the array to compute variance, you can use
    ``where``.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 1, 1, 0],
    ...                    [1, 1, 0, 1]], dtype=bool)
    >>> jnp.nanvar(x, axis=1, keepdims=True, where=where)
    Array([[2.25],
           [0.  ],
           [4.  ]], dtype=float32)
  """
  check_arraylike("nanvar", a)
  dtypes.check_user_dtype_supported(dtype, "nanvar")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanvar is not supported.")

  computation_dtype, dtype = _var_promote_types(dtypes.dtype(a), dtype)
  a = lax_internal.asarray(a).astype(computation_dtype)
  a_mean = nanmean(a, axis, dtype=computation_dtype, keepdims=True, where=where)

  centered = _where(lax_internal._isnan(a), 0, lax.sub(a, a_mean))  # double-where trick for gradients.
  if dtypes.issubdtype(centered.dtype, np.complexfloating):
    centered = lax.real(lax.mul(centered, lax.conj(centered)))
  else:
    centered = lax.square(centered)

  normalizer = sum(lax_internal.bitwise_not(lax_internal._isnan(a)),
                   axis=axis, keepdims=keepdims, where=where)
  normalizer = normalizer - ddof
  normalizer_mask = lax.le(normalizer, lax_internal._zero(normalizer))
  result = sum(centered, axis, keepdims=keepdims, where=where)
  result = _where(normalizer_mask, np.nan, result)
  divisor = _where(normalizer_mask, 1, normalizer)
  result = lax.div(result, lax.convert_element_type(divisor, result.dtype))
  return lax.convert_element_type(result, dtype)
