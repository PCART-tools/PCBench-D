def pinv(a: ArrayLike, rtol: ArrayLike | None = None,
         hermitian: bool = False, *,
         rcond: ArrayLike | DeprecatedArg | None = DeprecatedArg()) -> Array:
  """Compute the (Moore-Penrose) pseudo-inverse of a matrix.

  JAX implementation of :func:`numpy.linalg.pinv`.

  Args:
    a: array of shape ``(..., M, N)`` containing matrices to pseudo-invert.
    rtol: float or array_like of shape ``a.shape[:-2]``. Specifies the cutoff
      for small singular values.of shape ``(...,)``.
      Cutoff for small singular values; singular values smaller
      ``rtol * largest_singular_value`` are treated as zero. The default is
      determined based on the floating point precision of the dtype.
    hermitian: if True, then the input is assumed to be Hermitian, and a more
      efficient algorithm is used (default: False)
    rcond: deprecated alias of the ``rtol`` argument. Will result in a
      :class:`DeprecationWarning` if used.

  Returns:
    An array of shape ``(..., N, M)`` containing the pseudo-inverse of ``a``.

  See also:
    - :func:`jax.numpy.linalg.inv`: multiplicative inverse of a square matrix.

  Notes:
    :func:`jax.numpy.linalg.prng` differs from :func:`numpy.linalg.prng` in the
    default value of `rcond``: in NumPy, the default  is `1e-15`. In JAX, the
    default is ``10. * max(num_rows, num_cols) * jnp.finfo(dtype).eps``.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4],
    ...                [5, 6]])
    >>> a_pinv = jnp.linalg.pinv(a)
    >>> a_pinv  # doctest: +SKIP
    Array([[-1.333332  , -0.33333257,  0.6666657 ],
           [ 1.0833322 ,  0.33333272, -0.41666582]], dtype=float32)

    The pseudo-inverse operates as a multiplicative inverse so long as the
    output is not rank-deficient:

    >>> jnp.allclose(a_pinv @ a, jnp.eye(2), atol=1E-4)
    Array(True, dtype=bool)
  """
  if not isinstance(rcond, DeprecatedArg):
    rtol = rcond
    del rcond
    deprecations.warn(
      "jax-numpy-linalg-pinv-rcond",
      ("The rcond argument for linalg.pinv is deprecated. "
       "Please use rtol instead."),
       stacklevel=2
    )

  return _pinv(a, rtol, hermitian)
