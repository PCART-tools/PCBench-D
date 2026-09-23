@partial(jit, static_argnames=('UPLO', 'symmetrize_input'))
def eigh(a: ArrayLike, UPLO: str | None = None,
         symmetrize_input: bool = True) -> EighResult:
  """
  Compute the eigenvalues and eigenvectors of a Hermitian matrix.

  JAX implementation of :func:`numpy.linalg.eigh`.

  Args:
    a: array of shape ``(..., M, M)``, containing the Hermitian (if complex)
      or symmetric (if real) matrix.
    UPLO: specifies whether the calculation is done with the lower triangular
      part of ``a`` (``'L'``, default) or the upper triangular part (``'U'``).
    symmetrize_input: if True (default) then input is symmetrized, which leads
      to better behavior under automatic differentiation.

  Returns:
    A namedtuple ``(eigenvalues, eigenvectors)`` where

    - ``eigenvalues``: an array of shape ``(..., M)`` containing the eigenvalues,
      sorted in ascending order.
    - ``eigenvectors``: an array of shape ``(..., M, M)``, where column ``v[:, i]`` is the
      normalized eigenvector corresponding to the eigenvalue ``w[i]``.

  See also:
    - :func:`jax.numpy.linalg.eig`: general eigenvalue decomposition.
    - :func:`jax.numpy.linalg.eigvalsh`: compute eigenvalues only.
    - :func:`jax.scipy.linalg.eigh`: SciPy API for Hermitian eigendecomposition.
    - :func:`jax.lax.linalg.eigh`: XLA API for Hermitian eigendecomposition.

  Examples:
    >>> a = jnp.array([[1, -2j],
    ...                [2j, 1]])
    >>> w, v = jnp.linalg.eigh(a)
    >>> w
    Array([-1.,  3.], dtype=float32)
    >>> with jnp.printoptions(precision=3):
    ...   v
    Array([[-0.707+0.j   , -0.707+0.j   ],
           [ 0.   +0.707j,  0.   -0.707j]], dtype=complex64)
  """
  check_arraylike("jnp.linalg.eigh", a)
  if UPLO is None or UPLO == "L":
    lower = True
  elif UPLO == "U":
    lower = False
  else:
    msg = f"UPLO must be one of None, 'L', or 'U', got {UPLO}"
    raise ValueError(msg)

  a, = promote_dtypes_inexact(jnp.asarray(a))
  v, w = lax_linalg.eigh(a, lower=lower, symmetrize_input=symmetrize_input)
  return EighResult(w, v)
