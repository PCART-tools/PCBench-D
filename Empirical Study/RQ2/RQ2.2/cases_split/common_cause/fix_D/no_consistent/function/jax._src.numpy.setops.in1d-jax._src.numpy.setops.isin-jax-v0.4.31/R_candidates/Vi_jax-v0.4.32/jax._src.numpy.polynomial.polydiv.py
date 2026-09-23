def polydiv(u: ArrayLike, v: ArrayLike, *, trim_leading_zeros: bool = False) -> tuple[Array, Array]:
  r"""Returns the quotient and remainder of polynomial division.

  JAX implementation of :func:`numpy.polydiv`.

  Args:
    u: Array of dividend polynomial coefficients.
    v: Array of divisor polynomial coefficients.
    trim_leading_zeros: Default is ``False``. If ``True`` removes the leading
      zeros in the return value to match the result of numpy. But prevents the
      function from being able to be used in compiled code. Due to differences
      in accumulation of floating point arithmetic errors, the cutoff for values
      to be considered zero may lead to inconsistent results between NumPy and
      JAX, and even between different JAX backends. The result may lead to
      inconsistent output shapes when ``trim_leading_zeros=True``.

  Returns:
    A tuple of quotient and remainder arrays. The dtype of the output is always
    promoted to inexact.

  Note:
    :func:`jax.numpy.polydiv` only accepts arrays as input unlike
    :func:`numpy.polydiv` which accepts scalar inputs as well.

  See also:
    - :func:`jax.numpy.polyadd`: Computes the sum of two polynomials.
    - :func:`jax.numpy.polysub`: Computes the difference of two polynomials.
    - :func:`jax.numpy.polymul`: Computes the product of two polynomials.

  Example:
    >>> x1 = jnp.array([5, 7, 9])
    >>> x2 = jnp.array([4, 1])
    >>> np.polydiv(x1, x2)
    (array([1.25  , 1.4375]), array([7.5625]))
    >>> jnp.polydiv(x1, x2)
    (Array([1.25  , 1.4375], dtype=float32), Array([0.    , 0.    , 7.5625], dtype=float32))

    If ``trim_leading_zeros=True``, the result matches with ``np.polydiv``'s.

    >>> jnp.polydiv(x1, x2, trim_leading_zeros=True)
    (Array([1.25  , 1.4375], dtype=float32), Array([7.5625], dtype=float32))
  """
  check_arraylike("polydiv", u, v)
  u_arr, v_arr = promote_dtypes_inexact(u, v)
  del u, v
  m = len(u_arr) - 1
  n = len(v_arr) - 1
  scale = 1. / v_arr[0]
  q: Array = zeros(max(m - n + 1, 1), dtype = u_arr.dtype) # force same dtype
  for k in range(0, m-n+1):
    d = scale * u_arr[k]
    q = q.at[k].set(d)
    u_arr = u_arr.at[k:k+n+1].add(-d*v_arr)
  if trim_leading_zeros:
    # use the square root of finfo(dtype) to approximate the absolute tolerance used in numpy
    u_arr = trim_zeros_tol(u_arr, tol=sqrt(finfo(u_arr.dtype).eps), trim='f')
  return q, u_arr
