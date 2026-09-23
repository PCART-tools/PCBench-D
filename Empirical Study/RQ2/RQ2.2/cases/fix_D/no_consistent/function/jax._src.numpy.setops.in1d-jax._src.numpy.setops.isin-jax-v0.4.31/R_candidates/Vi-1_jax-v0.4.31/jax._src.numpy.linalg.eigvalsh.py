@partial(jit, static_argnames=('UPLO',))
def eigvalsh(a: ArrayLike, UPLO: str | None = 'L') -> Array:
  """
  Compute the eigenvalues of a Hermitian matrix.

  JAX implementation of :func:`numpy.linalg.eigvalsh`.

  Args:
    a: array of shape ``(..., M, M)``, containing the Hermitian (if complex)
      or symmetric (if real) matrix.
    UPLO: specifies whether the calculation is done with the lower triangular
      part of ``a`` (``'L'``, default) or the upper triangular part (``'U'``).

  Returns:
    An array of shape ``(..., M)`` containing the eigenvalues, sorted in
    ascending order.

  See also:
    - :func:`jax.numpy.linalg.eig`: general eigenvalue decomposition.
    - :func:`jax.numpy.linalg.eigh`: computes eigenvalues and eigenvectors of a
      Hermitian matrix.

  Examples:
    >>> a = jnp.array([[1, -2j],
    ...                [2j, 1]])
    >>> w = jnp.linalg.eigvalsh(a)
    >>> w
    Array([-1.,  3.], dtype=float32)
  """
  check_arraylike("jnp.linalg.eigvalsh", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  w, _ = eigh(a, UPLO)
  return w
