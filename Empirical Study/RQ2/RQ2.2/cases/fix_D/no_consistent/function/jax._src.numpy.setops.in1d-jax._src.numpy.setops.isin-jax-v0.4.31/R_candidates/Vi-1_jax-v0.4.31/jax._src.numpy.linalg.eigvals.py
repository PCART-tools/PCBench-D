@jit
def eigvals(a: ArrayLike) -> Array:
  """
  Compute the eigenvalues of a general matrix.

  JAX implementation of :func:`numpy.linalg.eigvals`.

  Args:
    a: array of shape ``(..., M, M)`` for which to compute the eigenvalues.

  Returns:
    An array of shape ``(..., M)`` containing the eigenvalues.

  See also:
    - :func:`jax.numpy.linalg.eig`: computes eigenvalues eigenvectors of a general matrix.
    - :func:`jax.numpy.linalg.eigh`: computes eigenvalues eigenvectors of a Hermitian matrix.

  Notes:
    - This differs from :func:`numpy.linalg.eigvals` in that the return type of
      :func:`jax.numpy.linalg.eigvals` is always complex64 for 32-bit input, and
      complex128 for 64-bit input.
    - At present, non-symmetric eigendecomposition is only implemented on the CPU backend.

  Examples:
    >>> a = jnp.array([[1., 2.],
    ...                [2., 1.]])
    >>> w = jnp.linalg.eigvals(a)
    >>> with jnp.printoptions(precision=2):
    ...  w
    Array([ 3.+0.j, -1.+0.j], dtype=complex64)
  """
  check_arraylike("jnp.linalg.eigvals", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  return lax_linalg.eig(a, compute_left_eigenvectors=False,
                        compute_right_eigenvectors=False)[0]
