@_warn_on_positional_kwargs
def eig(x: ArrayLike, *, compute_left_eigenvectors: bool = True,
        compute_right_eigenvectors: bool = True) -> list[Array]:
  """Eigendecomposition of a general matrix.

  Nonsymmetric eigendecomposition is at present only implemented on CPU.
  """
  return eig_p.bind(x, compute_left_eigenvectors=compute_left_eigenvectors,
                    compute_right_eigenvectors=compute_right_eigenvectors)
