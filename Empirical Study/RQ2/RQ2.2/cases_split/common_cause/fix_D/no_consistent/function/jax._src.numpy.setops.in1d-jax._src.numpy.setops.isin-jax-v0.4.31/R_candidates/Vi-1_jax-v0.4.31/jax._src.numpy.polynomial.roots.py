def roots(p: ArrayLike, *, strip_zeros: bool = True) -> Array:
  r"""Returns the roots of a polynomial given the coefficients ``p``.

  JAX implementations of :func:`numpy.roots`.

  Args:
    p: Array of polynomial coefficients having rank-1.
    strip_zeros : bool, default=True. If True, then leading zeros in the
      coefficients will be stripped, similar to :func:`numpy.roots`. If set to
      False, leading zeros will not be stripped, and undefined roots will be
      represented by NaN values in the function output. ``strip_zeros`` must be
      set to ``False`` for the function to be compatible with :func:`jax.jit` and
      other JAX transformations.

  Returns:
    An array containing the roots of the polynomial.

  Note:
    Unlike ``np.roots`` of this function, the ``jnp.roots`` returns the roots
    in a complex array regardless of the values of the roots.

  See Also:
    - :func:`jax.numpy.poly`: Finds the polynomial coefficients of the given
      sequence of roots.
    - :func:`jax.numpy.polyfit`: Least squares polynomial fit to data.
    - :func:`jax.numpy.polyval`: Evaluate a polynomial at specific values.

  Examples:
    >>> coeffs = jnp.array([0, 1, 2])

    The default behavior matches numpy and strips leading zeros:

    >>> jnp.roots(coeffs)
    Array([-2.+0.j], dtype=complex64)

    With ``strip_zeros=False``, extra roots are set to NaN:

    >>> jnp.roots(coeffs, strip_zeros=False)
    Array([-2. +0.j, nan+nanj], dtype=complex64)
  """
  check_arraylike("roots", p)
  p_arr = atleast_1d(promote_dtypes_inexact(p)[0])
  del p
  if p_arr.ndim != 1:
    raise ValueError("Input must be a rank-1 array.")
  if p_arr.size < 2:
    return array([], dtype=dtypes.to_complex_dtype(p_arr.dtype))
  num_leading_zeros = _where(all(p_arr == 0), len(p_arr), argmin(p_arr == 0))

  if strip_zeros:
    num_leading_zeros = core.concrete_or_error(int, num_leading_zeros,
      "The error occurred in the jnp.roots() function. To use this within a "
      "JIT-compiled context, pass strip_zeros=False, but be aware that leading zeros "
      "will result in some returned roots being set to NaN.")
    return _roots_no_zeros(p_arr[num_leading_zeros:])
  else:
    return _roots_with_zeros(p_arr, num_leading_zeros)
