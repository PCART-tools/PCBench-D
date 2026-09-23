def eigh_jacobi(x: ArrayLike, *, lower: bool = True,
                sort_eigenvalues: bool = True) -> tuple[Array, Array]:
  """Helper Jacobi eigendecomposition implemented by XLA.

  Used as a subroutine of QDWH-eig on TPU."""
  w, v = eigh_jacobi_p.bind(x, lower=lower, sort_eigenvalues=sort_eigenvalues)
  return w, v
