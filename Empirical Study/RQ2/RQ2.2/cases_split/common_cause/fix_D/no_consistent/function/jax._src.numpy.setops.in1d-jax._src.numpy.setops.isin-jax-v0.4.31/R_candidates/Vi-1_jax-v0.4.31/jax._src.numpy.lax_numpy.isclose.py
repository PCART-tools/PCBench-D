@partial(jit, static_argnames=('equal_nan',))
def isclose(a: ArrayLike, b: ArrayLike, rtol: ArrayLike = 1e-05, atol: ArrayLike = 1e-08,
            equal_nan: bool = False) -> Array:
  r"""Check if the elements of two arrays are approximately equal within a tolerance.

  JAX implementation of :func:`numpy.allclose`.

  Essentially this function evaluates the following condition:

  .. math::

     |a - b| \le \mathtt{atol} + \mathtt{rtol} * |b|

  ``jnp.inf`` in ``a`` will be considered equal to ``jnp.inf`` in ``b``.

  Args:
    a: first input array to compare.
    b: second input array to compare.
    rtol: relative tolerance used for approximate equality. Default = 1e-05.
    atol: absolute tolerance used for approximate equality. Default = 1e-08.
    equal_nan: Boolean. If ``True``, NaNs in ``a`` will be considered
      equal to NaNs in ``b``. Default is ``False``.

  Returns:
    A new array containing boolean values indicating whether the input arrays
    are element-wise approximately equal within the specified tolerances.

  See Also:
    - :func:`jax.numpy.allclose`
    - :func:`jax.numpy.equal`

  Examples:
    >>> jnp.isclose(jnp.array([1e6, 2e6, jnp.inf]), jnp.array([1e6, 2e7, jnp.inf]))
    Array([ True, False,  True], dtype=bool)
    >>> jnp.isclose(jnp.array([1e6, 2e6, 3e6]),
    ...              jnp.array([1.00008e6, 2.00008e7, 3.00008e8]), rtol=1e3)
    Array([ True,  True,  True], dtype=bool)
    >>> jnp.isclose(jnp.array([1e6, 2e6, 3e6]),
    ...              jnp.array([1.00001e6, 2.00002e6, 3.00009e6]), atol=1e3)
    Array([ True,  True,  True], dtype=bool)
    >>> jnp.isclose(jnp.array([jnp.nan, 1, 2]),
    ...              jnp.array([jnp.nan, 1, 2]), equal_nan=True)
    Array([ True,  True,  True], dtype=bool)
  """
  a, b = util.promote_args("isclose", a, b)
  dtype = _dtype(a)
  if dtypes.issubdtype(dtype, dtypes.extended):
    return lax.eq(a, b)

  a, b = util.promote_args_inexact("isclose", a, b)
  dtype = _dtype(a)
  if issubdtype(dtype, complexfloating):
    dtype = util._complex_elem_type(dtype)
  rtol = lax.convert_element_type(rtol, dtype)
  atol = lax.convert_element_type(atol, dtype)
  out = lax.le(
    lax.abs(lax.sub(a, b)),
    lax.add(atol, lax.mul(rtol, lax.abs(b))))
  # This corrects the comparisons for infinite and nan values
  a_inf = ufuncs.isinf(a)
  b_inf = ufuncs.isinf(b)
  any_inf = ufuncs.logical_or(a_inf, b_inf)
  both_inf = ufuncs.logical_and(a_inf, b_inf)
  # Make all elements where either a or b are infinite to False
  out = ufuncs.logical_and(out, ufuncs.logical_not(any_inf))
  # Make all elements where both a or b are the same inf to True
  same_value = lax.eq(a, b)
  same_inf = ufuncs.logical_and(both_inf, same_value)
  out = ufuncs.logical_or(out, same_inf)

  # Make all elements where either a or b is NaN to False
  a_nan = ufuncs.isnan(a)
  b_nan = ufuncs.isnan(b)
  any_nan = ufuncs.logical_or(a_nan, b_nan)
  out = ufuncs.logical_and(out, ufuncs.logical_not(any_nan))
  if equal_nan:
    # Make all elements where both a and b is NaN to True
    both_nan = ufuncs.logical_and(a_nan, b_nan)
    out = ufuncs.logical_or(out, both_nan)
  return out
