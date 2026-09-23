@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanstd(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
           ddof: int = 0, keepdims: bool = False,
           where: ArrayLike | None = None) -> Array:
  r"""Compute the standard deviation along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanstd`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      standard deviation is computed. If None, standard deviaiton is computed
      along flattened array.
    dtype: The type of the output array. Default=None.
    ddof: int, default=0. Degrees of freedom. The divisor in the standard deviation
      computation is ``N-ddof``, ``N`` is number of elements along given axis.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      standard deviation. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array containing the standard deviation of array elements along the given
    axis. If all elements along the given axis are NaNs, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements over a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanvar`: Compute the variance along the given axis, ignoring
      NaNs values.
    - :func:`jax.numpy.std`: Computed the standard deviation along the given axis.

  Examples:
    By default, ``jnp.nanstd`` computes the standard deviation along flattened array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[3, nan, 4, 5],
    ...                [nan, 2, nan, 7],
    ...                [2, 1, 6, nan]])
    >>> jnp.nanstd(x)
    Array(1.9843135, dtype=float32)

    If ``axis=0``, computes standard deviation along axis 0.

    >>> jnp.nanstd(x, axis=0)
    Array([0.5, 0.5, 1. , 1. ], dtype=float32)

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> jnp.nanstd(x, axis=0, keepdims=True)
    Array([[0.5, 0.5, 1. , 1. ]], dtype=float32)

    If ``ddof=1``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.nanstd(x, axis=0, keepdims=True, ddof=1))
    [[0.71 0.71 1.41 1.41]]

    To include specific elements of the array to compute standard deviation, you
    can use ``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 1, 0, 1],
    ...                  [1, 1, 0, 1]], dtype=bool)
    >>> jnp.nanstd(x, axis=0, keepdims=True, where=where)
    Array([[0.5, 0.5, 0. , 0. ]], dtype=float32)
  """
  check_arraylike("nanstd", a)
  dtypes.check_user_dtype_supported(dtype, "nanstd")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanstd is not supported.")
  return lax.sqrt(nanvar(a, axis=axis, dtype=dtype, ddof=ddof, keepdims=keepdims, where=where))
