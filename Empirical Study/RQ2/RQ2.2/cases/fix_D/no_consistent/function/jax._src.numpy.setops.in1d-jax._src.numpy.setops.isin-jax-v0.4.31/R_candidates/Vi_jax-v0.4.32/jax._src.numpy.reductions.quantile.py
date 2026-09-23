@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation', 'keepdims', 'method'))
def quantile(a: ArrayLike, q: ArrayLike, axis: int | tuple[int, ...] | None = None,
             out: None = None, overwrite_input: bool = False, method: str = "linear",
             keepdims: bool = False, *, interpolation: DeprecatedArg | str = DeprecatedArg()) -> Array:
  """Compute the quantile of the data along the specified axis.

  JAX implementation of :func:`numpy.quantile`.

  Args:
    a: N-dimensional array input.
    q: scalar or 1-dimensional array specifying the desired quantiles. ``q``
      should contain floating-point values between ``0.0`` and ``1.0``.
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
    An array containing the specified quantiles along the specified axes.

  See also:
    - :func:`jax.numpy.nanquantile`: compute the quantile while ignoring NaNs
    - :func:`jax.numpy.percentile`: compute the percentile (0-100)

  Examples:
    Computing the median and quartiles of an array, with linear interpolation:

    >>> x = jnp.arange(10)
    >>> q = jnp.array([0.25, 0.5, 0.75])
    >>> jnp.quantile(x, q)
    Array([2.25, 4.5 , 6.75], dtype=float32)

    Computing the quartiles using nearest-value interpolation:

    >>> jnp.quantile(x, q, method='nearest')
    Array([2., 4., 7.], dtype=float32)
  """
  check_arraylike("quantile", a, q)
  if overwrite_input or out is not None:
    raise ValueError("jax.numpy.quantile does not support overwrite_input=True "
                     "or out != None")
  if not isinstance(interpolation, DeprecatedArg):
    deprecations.warn(
      "jax-numpy-quantile-interpolation",
      ("The interpolation= argument to 'quantile' is deprecated. "
       "Use 'method=' instead."), stacklevel=2)
    method = interpolation
  return _quantile(lax_internal.asarray(a), lax_internal.asarray(q), axis, method, keepdims, False)
