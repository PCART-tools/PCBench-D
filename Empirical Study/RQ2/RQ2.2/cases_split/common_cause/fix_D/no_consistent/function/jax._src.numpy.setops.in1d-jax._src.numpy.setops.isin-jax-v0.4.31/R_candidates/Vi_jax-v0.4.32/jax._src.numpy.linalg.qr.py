@partial(jit, static_argnames=('mode',))
def qr(a: ArrayLike, mode: str = "reduced") -> Array | QRResult:
  """Compute the QR decomposition of an array

  JAX implementation of :func:`numpy.linalg.qr`.

  The QR decomposition of a matrix `A` is given by

  .. math::

     A = QR

  Where `Q` is a unitary matrix (i.e. :math:`Q^HQ=I`) and `R` is an upper-triangular
  matrix.

  Args:
    a: array of shape (..., M, N)
    mode: Computational mode. Supported values are:

      - ``"reduced"`` (default): return `Q` of shape ``(..., M, K)`` and `R` of shape
        ``(..., K, N)``, where ``K = min(M, N)``.
      - ``"complete"``: return `Q` of shape ``(..., M, M)`` and `R` of shape ``(..., M, N)``.
      - ``"raw"``: return lapack-internal representations of shape ``(..., M, N)`` and ``(..., K)``.
      - ``"r"``: return `R` only.

  Returns:
    A tuple ``(Q, R)`` (if ``mode`` is not ``"r"``) otherwise an array ``R``,
    where:

    - ``Q`` is an orthogonal matrix of shape ``(..., M, K)`` (if ``mode`` is ``"reduced"``)
      or ``(..., M, M)`` (if ``mode`` is ``"complete"``).
    - ``R`` is an upper-triangular matrix of shape ``(..., M, N)`` (if ``mode`` is
      ``"r"`` or ``"complete"``) or ``(..., K, N)`` (if ``mode`` is ``"reduced"``)

    with ``K = min(M, N)``.

  See also:
    - :func:`jax.scipy.linalg.qr`: SciPy-style QR decomposition API
    - :func:`jax.lax.linalg.qr`: XLA-style QR decomposition API

  Examples:
    Compute the QR decomposition of a matrix:

    >>> a = jnp.array([[1., 2., 3., 4.],
    ...                [5., 4., 2., 1.],
    ...                [6., 3., 1., 5.]])
    >>> Q, R = jnp.linalg.qr(a)
    >>> Q  # doctest: +SKIP
    Array([[-0.12700021, -0.7581426 , -0.6396022 ],
           [-0.63500065, -0.43322435,  0.63960224],
           [-0.7620008 ,  0.48737738, -0.42640156]], dtype=float32)
    >>> R  # doctest: +SKIP
    Array([[-7.8740077, -5.080005 , -2.4130025, -4.953006 ],
           [ 0.       , -1.7870499, -2.6534991, -1.028908 ],
           [ 0.       ,  0.       , -1.0660033, -4.050814 ]], dtype=float32)

    Check that ``Q`` is orthonormal:

    >>> jnp.allclose(Q.T @ Q, jnp.eye(3), atol=1E-5)
    Array(True, dtype=bool)

    Reconstruct the input:

    >>> jnp.allclose(Q @ R, a)
    Array(True, dtype=bool)
  """
  check_arraylike("jnp.linalg.qr", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  if mode == "raw":
    a, taus = lax_linalg.geqrf(a)
    return QRResult(a.mT, taus)
  if mode in ("reduced", "r", "full"):
    full_matrices = False
  elif mode == "complete":
    full_matrices = True
  else:
    raise ValueError(f"Unsupported QR decomposition mode '{mode}'")
  q, r = lax_linalg.qr(a, full_matrices=full_matrices)
  if mode == "r":
    return r
  return QRResult(q, r)
