@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'keepdims'))
def nanmedian(a: ArrayLike, axis: int | tuple[int, ...] | None = None,
              out: None = None, overwrite_input: bool = False,
              keepdims: bool = False) -> Array:
  r"""Return the median of array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanmedian`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      median to be computed. If None, median is computed for the flattened array.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    out: Unused by JAX.
    overwrite_input: Unused by JAX.

  Returns:
    An array containing the median along the given axis, ignoring NaNs. If all
    elements along the given axis are NaNs, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements over a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements over given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements over given
      axis, ignoring NaNs.

  Examples:
    By default, the median is computed for the flattened array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[2, nan, 7, nan],
    ...                [nan, 5, 9, 2],
    ...                [6, 1, nan, 3]])
    >>> jnp.nanmedian(x)
    Array(4., dtype=float32)

    If ``axis=1``, the median is computed along axis 1.

    >>> jnp.nanmedian(x, axis=1)
    Array([4.5, 5. , 3. ], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output is equal to that of the input.

    >>> jnp.nanmedian(x, axis=1, keepdims=True)
    Array([[4.5],
           [5. ],
           [3. ]], dtype=float32)
  """
  check_arraylike("nanmedian", a)
  return nanquantile(a, 0.5, axis=axis, out=out,
                     overwrite_input=overwrite_input, keepdims=keepdims,
                     method='midpoint')
