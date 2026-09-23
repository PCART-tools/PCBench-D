@partial(jit, static_argnames=('m',))
def polyder(p: ArrayLike, m: int = 1) -> Array:
  r"""Returns the coefficients of the derivative of specified order of a polynomial.

  JAX implementation of :func:`numpy.polyder`.

  Args:
    p: Array of polynomials coefficients.
    m: Order of differentiation (positive integer). Default is 1. It must be
      specified statically.

  Returns:
    An array of polynomial coefficients representing the derivative.

  Note:
    :func:`jax.numpy.polyder` differs from :func:`numpy.polyder` when an integer
    array is given. NumPy returns the result with dtype ``int`` whereas JAX
    returns the result with dtype ``float``.

  See also:
    - :func:`jax.numpy.polyint`: Computes the integral of polynomial.
    - :func:`jax.numpy.polyval`: Evaluates a polynomial at specific values.

  Examples:

    The first order derivative of the polynomial :math:`2 x^3 - 5 x^2 + 3 x - 1`
    is :math:`6 x^2 - 10 x +3`:

    >>> p = jnp.array([2, -5, 3, -1])
    >>> jnp.polyder(p)
    Array([  6., -10.,   3.], dtype=float32)

    and its second order derivative is :math:`12 x - 10`:

    >>> jnp.polyder(p, m=2)
    Array([ 12., -10.], dtype=float32)
  """
  check_arraylike("polyder", p)
  m = core.concrete_or_error(operator.index, m, "'m' argument of jnp.polyder")
  p_arr, = promote_dtypes_inexact(p)
  del p
  if m < 0:
    raise ValueError("Order of derivative must be positive")
  if m == 0:
    return p_arr
  coeff = (arange(m, len(p_arr), dtype=p_arr.dtype)[np.newaxis]
          - arange(m, dtype=p_arr.dtype)[:, np.newaxis]).prod(0)
  return p_arr[:-m] * coeff[::-1]
