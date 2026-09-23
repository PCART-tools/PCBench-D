@partial(jit, static_argnames=('m',))
def polyint(p: ArrayLike, m: int = 1, k: int | ArrayLike | None = None) -> Array:
  r"""Returns the coefficients of the integration of specified order of a polynomial.

  JAX implementation of :func:`numpy.polyint`.

  Args:
    p: An array of polynomial coefficients.
    m: Order of integration. Default is 1. It must be specified statically.
    k: Scalar or array of ``m`` integration constant (s).

  Returns:
    An array of coefficients of integrated polynomial.

  See also:
    - :func:`jax.numpy.polyder`: Computes the coefficients of the derivative of
      a polynomial.
    - :func:`jax.numpy.polyval`: Evaluates a polynomial at specific values.

  Examples:

    The first order integration of the polynomial :math:`12 x^2 + 12 x + 6` is
    :math:`4 x^3 + 6 x^2 + 6 x`.

    >>> p = jnp.array([12, 12, 6])
    >>> jnp.polyint(p)
    Array([4., 6., 6., 0.], dtype=float32)

    Since the constant ``k`` is not provided, the result included ``0`` at the end.
    If the constant ``k`` is provided:

    >>> jnp.polyint(p, k=4)
    Array([4., 6., 6., 4.], dtype=float32)

    and the second order integration is :math:`x^4 + 2 x^3 + 3 x`:

    >>> jnp.polyint(p, m=2)
    Array([1., 2., 3., 0., 0.], dtype=float32)

    When ``m>=2``, the constants ``k`` should be provided as an array having
    ``m`` elements. The second order integration of the polynomial
    :math:`12 x^2 + 12 x + 6` with the constants ``k=[4, 5]`` is
    :math:`x^4 + 2 x^3 + 3 x^2 + 4 x + 5`:

    >>> jnp.polyint(p, m=2, k=jnp.array([4, 5]))
    Array([1., 2., 3., 4., 5.], dtype=float32)
  """
  m = core.concrete_or_error(operator.index, m, "'m' argument of jnp.polyint")
  k = 0 if k is None else k
  check_arraylike("polyint", p, k)
  p_arr, k_arr = promote_dtypes_inexact(p, k)
  del p, k
  if m < 0:
    raise ValueError("Order of integral must be positive (see polyder)")
  k_arr = atleast_1d(k_arr)
  if len(k_arr) == 1:
    k_arr = full((m,), k_arr[0])
  if k_arr.shape != (m,):
    raise ValueError("k must be a scalar or a rank-1 array of length 1 or m.")
  if m == 0:
    return p_arr
  else:
    grid = (arange(len(p_arr) + m, dtype=p_arr.dtype)[np.newaxis]
            - arange(m, dtype=p_arr.dtype)[:, np.newaxis])
    coeff = maximum(1, grid).prod(0)[::-1]
    return true_divide(concatenate((p_arr, k_arr)), coeff)
