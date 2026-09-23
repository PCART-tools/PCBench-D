@partial(jit, static_argnames=('method',))
def slogdet(a: ArrayLike, *, method: str | None = None) -> SlogdetResult:
  """
  Compute the sign and (natural) logarithm of the determinant of an array.

  JAX implementation of :func:`numpy.linalg.slogdet`.

  Args:
    a: array of shape ``(..., M, M)`` for which to compute the sign and log determinant.
    method: the method to use for determinant computation. Options are

      - ``'lu'`` (default): use the LU decomposition.
      - ``'qr'``: use the QR decomposition.

  Returns:
    A tuple of arrays ``(sign, logabsdet)``, each of shape ``a.shape[:-2]``

    - ``sign`` is the sign of the determinant.
    - ``logabsdet`` is the natural log of the determinant's absolute value.

  See also:
    :func:`jax.numpy.linalg.det`: direct computation of determinant

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> sign, logabsdet = jnp.linalg.slogdet(a)
    >>> sign  # -1 indicates negative determinant
    Array(-1., dtype=float32)
    >>> jnp.exp(logabsdet)  # Absolute value of determinant
    Array(2., dtype=float32)
  """
  check_arraylike("jnp.linalg.slogdet", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  a_shape = jnp.shape(a)
  if len(a_shape) < 2 or a_shape[-1] != a_shape[-2]:
    raise ValueError("Argument to slogdet() must have shape [..., n, n], got {a_shape}")
  if method is None or method == "lu":
    return SlogdetResult(*_slogdet_lu(a))
  elif method == "qr":
    return SlogdetResult(*_slogdet_qr(a))
  else:
    raise ValueError(f"Unknown slogdet method '{method}'. Supported methods "
                     "are 'lu' (`None`), and 'qr'.")
