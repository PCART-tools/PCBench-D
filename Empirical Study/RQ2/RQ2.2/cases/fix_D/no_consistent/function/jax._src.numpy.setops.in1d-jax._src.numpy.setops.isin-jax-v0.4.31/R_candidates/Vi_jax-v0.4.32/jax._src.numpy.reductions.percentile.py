@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation', 'keepdims', 'method'))
def percentile(a: ArrayLike, q: ArrayLike,
               axis: int | tuple[int, ...] | None = None,
               out: None = None, overwrite_input: bool = False, method: str = "linear",
               keepdims: bool = False, *, interpolation: str | DeprecatedArg = DeprecatedArg()) -> Array:
  """Compute the percentile of the data along the specified axis.

  JAX implementation of :func:`numpy.percentile`.

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
    - :func:`jax.numpy.quantile`: compute the quantile (0.0-1.0)
    - :func:`jax.numpy.nanpercentile`: compute the percentile while ignoring NaNs

  Examples:
    Computing the median and quartiles of a 1D array:

    >>> x = jnp.array([0, 1, 2, 3, 4, 5, 6])
    >>> q = jnp.array([25, 50, 75])
    >>> jnp.percentile(x, q)
    Array([1.5, 3. , 4.5], dtype=float32)

    Computing the same percentiles with nearest rather than linear interpolation:

    >>> jnp.percentile(x, q, method='nearest')
    Array([1., 3., 4.], dtype=float32)
  """
  check_arraylike("percentile", a, q)
  q, = promote_dtypes_inexact(q)
  if not isinstance(interpolation, DeprecatedArg):
    deprecations.warn(
      "jax-numpy-quantile-interpolation",
      ("The interpolation= argument to 'percentile' is deprecated. "
       "Use 'method=' instead."), stacklevel=2)
    method = interpolation
  return quantile(a, q / 100, axis=axis, out=out, overwrite_input=overwrite_input,
                  method=method, keepdims=keepdims)
