def polymul(a1: ArrayLike, a2: ArrayLike, *, trim_leading_zeros: bool = False) -> Array:
  r"""Returns the product of two polynomials.

  JAX implementation of :func:`numpy.polymul`.

  Args:
    a1: 1D array of polynomial coefficients.
    a2: 1D array of polynomial coefficients.
    trim_leading_zeros: Default is ``False``. If ``True`` removes the leading
      zeros in the return value to match the result of numpy. But prevents the
      function from being able to be used in compiled code. Due to differences
      in accumulation of floating point arithmetic errors, the cutoff for values
      to be considered zero may lead to inconsistent results between NumPy and
      JAX, and even between different JAX backends. The result may lead to
      inconsistent output shapes when ``trim_leading_zeros=True``.

  Returns:
    An array of the coefficients of the product of the two polynomials. The dtype
    of the output is always promoted to inexact.

  Note:
    :func:`jax.numpy.polymul` only accepts arrays as input unlike
    :func:`numpy.polymul` which accepts scalar inputs as well.

  See also:
    - :func:`jax.numpy.polyadd`: Computes the sum of two polynomials.
    - :func:`jax.numpy.polysub`: Computes the difference of two polynomials.
    - :func:`jax.numpy.polydiv`: Computes the quotient and remainder of polynomial
      division.

  Example:
    >>> x1 = np.array([2, 1, 0])
    >>> x2 = np.array([0, 5, 0, 3])
    >>> np.polymul(x1, x2)
    array([10,  5,  6,  3,  0])
    >>> jnp.polymul(x1, x2)
    Array([ 0., 10.,  5.,  6.,  3.,  0.], dtype=float32)

    If ``trim_leading_zeros=True``, the result matches with ``np.polymul``'s.

    >>> jnp.polymul(x1, x2, trim_leading_zeros=True)
    Array([10.,  5.,  6.,  3.,  0.], dtype=float32)

    For input arrays of dtype ``complex``:

    >>> x3 = np.array([2., 1+2j, 1-2j])
    >>> x4 = np.array([0, 5, 0, 3])
    >>> np.polymul(x3, x4)
    array([10. +0.j,  5.+10.j, 11.-10.j,  3. +6.j,  3. -6.j])
    >>> jnp.polymul(x3, x4)
    Array([ 0. +0.j, 10. +0.j,  5.+10.j, 11.-10.j,  3. +6.j,  3. -6.j],      dtype=complex64)
    >>> jnp.polymul(x3, x4, trim_leading_zeros=True)
    Array([10. +0.j,  5.+10.j, 11.-10.j,  3. +6.j,  3. -6.j], dtype=complex64)
  """
  check_arraylike("polymul", a1, a2)
  a1_arr, a2_arr = promote_dtypes_inexact(a1, a2)
  del a1, a2
  if trim_leading_zeros and (len(a1_arr) > 1 or len(a2_arr) > 1):
    a1_arr, a2_arr = trim_zeros(a1_arr, trim='f'), trim_zeros(a2_arr, trim='f')
  if len(a1_arr) == 0:
    a1_arr = asarray([0], dtype=a2_arr.dtype)
  if len(a2_arr) == 0:
    a2_arr = asarray([0], dtype=a1_arr.dtype)
  return convolve(a1_arr, a2_arr, mode='full')
