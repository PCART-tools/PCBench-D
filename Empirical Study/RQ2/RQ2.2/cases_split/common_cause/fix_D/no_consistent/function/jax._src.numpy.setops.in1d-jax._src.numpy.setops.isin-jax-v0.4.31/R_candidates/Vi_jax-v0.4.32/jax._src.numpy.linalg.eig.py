def eig(a: ArrayLike) -> tuple[Array, Array]:
  """
  Compute the eigenvalues and eigenvectors of a square array.

  JAX implementation of :func:`numpy.linalg.eig`.

  Args:
    a: array of shape ``(..., M, M)`` for which to compute the eigenvalues and vectors.

  Returns:
    A tuple ``(eigenvalues, eigenvectors)`` with

    - ``eigenvalues``: an array of shape ``(..., M)`` containing the eigenvalues.
    - ``eigenvectors``: an array of shape ``(..., M, M)``, where column ``v[:, i]`` is the
      eigenvector corresponding to the eigenvalue ``w[i]``.

  Notes:
    - This differs from :func:`numpy.linalg.eig` in that the return type of
      :func:`jax.numpy.linalg.eig` is always complex64 for 32-bit input, and complex128
      for 64-bit input.
    - At present, non-symmetric eigendecomposition is only implemented on the CPU backend.

  See also:
    - :func:`jax.numpy.linalg.eigh`: eigenvectors and eigenvalues of a Hermitian matrix.
    - :func:`jax.numpy.linalg.eigvals`: compute eigenvalues only.

  Examples:
    >>> a = jnp.array([[1., 2.],
    ...                [2., 1.]])
    >>> w, v = jnp.linalg.eig(a)
    >>> with jax.numpy.printoptions(precision=4):
    ...   w
    Array([ 3.+0.j, -1.+0.j], dtype=complex64)
    >>> v
    Array([[ 0.70710677+0.j, -0.70710677+0.j],
           [ 0.70710677+0.j,  0.70710677+0.j]], dtype=complex64)
  """
  check_arraylike("jnp.linalg.eig", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  w, v = lax_linalg.eig(a, compute_left_eigenvectors=False)
  return w, v
