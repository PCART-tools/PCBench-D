@_warn_on_positional_kwargs
def cholesky(x, *, symmetrize_input: bool = True):
  """Cholesky decomposition.

  Computes the Cholesky decomposition

  .. math::
    A = L . L^H

  of square matrices, :math:`A`, such that :math:`L`
  is lower triangular. The matrices of :math:`A` must be positive-definite and
  either Hermitian, if complex, or symmetric, if real.

  Args:
    x: A batch of square Hermitian (symmetric if real) positive-definite
      matrices with shape ``[..., n, n]``.
    symmetrize_input: If ``True``, the matrix is symmetrized before Cholesky
      decomposition by computing :math:`\\frac{1}{2}(x + x^H)`. If ``False``,
      only the lower triangle of ``x`` is used; the upper triangle is ignored
      and not accessed.

  Returns:
    The Cholesky decomposition as a matrix with the same dtype as ``x`` and
    shape ``[..., n, n]``. If Cholesky decomposition fails, returns a matrix
    full of NaNs. The behavior on failure may change in the future.
  """
  if symmetrize_input:
    x = symmetrize(x)
  return jnp.tril(cholesky_p.bind(x))
