@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation', 'keepdims', 'method'))
def nanpercentile(a: ArrayLike, q: ArrayLike,
                  axis: int | tuple[int, ...] | None = None,
                  out: None = None, overwrite_input: bool = False, method: str = "linear",
                  keepdims: bool = False, *, interpolation: str | DeprecatedArg = DeprecatedArg()) -> Array:
  """Compute the percentile of the data along the specified axis, ignoring NaN values.

  JAX implementation of :func:`numpy.nanpercentile`.

  Args:
    a: N-dimensional array input.
    q: scalar or 1-dimensional array specifying the desired quantiles. ``q``
      should contain integer or floating point values between ``0`` and ``100``.
    axis: optional axis or tuple of axes along which to compute the quantile
    out: not implemented by JAX; will error if not None
    overwrite_input: not implemented by JAX; will error if not False
    method: specify the interpolation method to use. Options are one of
      ``["linear", "lower", "higher", "midpoint", "nearest"]``.
      default is ``linear``.
    keepdims: if True, then the returned array will have the same number of
      dimensions as the input. Default is False.
    interpolation: deprecated alias of the ``method`` argument. Will result
      in a :class:`DeprecationWarning` if used.

  Returns:
    An array containing the specified percentiles along the specified axes.

  See also:
    - :func:`jax.numpy.nanquantile`: compute the nan-aware quantile (0.0-1.0)
    - :func:`jax.numpy.percentile`: compute the percentile without special
      handling of NaNs.

  Examples:
    Computing the median and quartiles of a 1D array:

    >>> x = jnp.array([0, 1, 2, jnp.nan, 3, 4, 5, 6])
    >>> q = jnp.array([25, 50, 75])

    Because of the NaN value, :func:`jax.numpy.percentile` returns all NaNs,
    while :func:`~jax.numpy.nanpercentile` ignores them:

    >>> jnp.percentile(x, q)
    Array([nan, nan, nan], dtype=float32)
    >>> jnp.nanpercentile(x, q)
    Array([1.5, 3. , 4.5], dtype=float32)
  """
  check_arraylike("nanpercentile", a, q)
  q, = promote_dtypes_inexact(q)
  q = q / 100
  if not isinstance(interpolation, DeprecatedArg):
    deprecations.warn(
      "jax-numpy-quantile-interpolation",
      ("The interpolation= argument to 'nanpercentile' is deprecated. "
       "Use 'method=' instead."), stacklevel=2)
    method = interpolation
  return nanquantile(a, q, axis=axis, out=out, overwrite_input=overwrite_input,
                     method=method, keepdims=keepdims)
