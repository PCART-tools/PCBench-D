@partial(jit, static_argnames=('decimals',))
def round(a: ArrayLike, decimals: int = 0, out: None = None) -> Array:
  """Round input evenly to the given number of decimals.

  JAX implementation of :func:`numpy.round`.

  Args:
    a: input array or scalar.
    decimals: int, default=0. Number of decimal points to which the input needs
      to be rounded. It must be specified statically. Not implemented for
      ``decimals < 0``.
    out: Unused by JAX.

  Returns:
    An array containing the rounded values to the specified ``decimals`` with
    same shape and dtype as ``a``.

  Note:
    ``jnp.round`` rounds to the nearest even integer for the values exactly halfway
    between rounded decimal values.

  See also:
    - :func:`jax.numpy.floor`: Rounds the input to the nearest integer downwards.
    - :func:`jax.numpy.ceil`: Rounds the input to the nearest integer upwards.
    - :func:`jax.numpy.fix` and :func:numpy.trunc`: Rounds the input to the
      nearest integer towards zero.

  Examples:
    >>> x = jnp.array([1.532, 3.267, 6.149])
    >>> jnp.round(x)
    Array([2., 3., 6.], dtype=float32)
    >>> jnp.round(x, decimals=2)
    Array([1.53, 3.27, 6.15], dtype=float32)

    For values exactly halfway between rounded values:

    >>> x1 = jnp.array([10.5, 21.5, 12.5, 31.5])
    >>> jnp.round(x1)
    Array([10., 22., 12., 32.], dtype=float32)
  """
  util.check_arraylike("round", a)
  decimals = core.concrete_or_error(operator.index, decimals, "'decimals' argument of jnp.round")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.round is not supported.")
  dtype = _dtype(a)
  if issubdtype(dtype, integer):
    if decimals < 0:
      raise NotImplementedError(
        "integer np.round not implemented for decimals < 0")
    return asarray(a)  # no-op on integer types

  def _round_float(x: ArrayLike) -> Array:
    if decimals == 0:
      return lax.round(x, lax.RoundingMethod.TO_NEAREST_EVEN)

    # TODO(phawkins): the strategy of rescaling the value isn't necessarily a
    # good one since we may be left with an incorrectly rounded value at the
    # end due to precision problems. As a workaround for float16, convert to
    # float32,
    x = lax.convert_element_type(x, np.float32) if dtype == np.float16 else x
    factor = _lax_const(x, 10 ** decimals)
    out = lax.div(lax.round(lax.mul(x, factor),
                            lax.RoundingMethod.TO_NEAREST_EVEN), factor)
    return lax.convert_element_type(out, dtype) if dtype == np.float16 else out

  if issubdtype(dtype, complexfloating):
    return lax.complex(_round_float(lax.real(a)), _round_float(lax.imag(a)))
  else:
    return _round_float(a)
