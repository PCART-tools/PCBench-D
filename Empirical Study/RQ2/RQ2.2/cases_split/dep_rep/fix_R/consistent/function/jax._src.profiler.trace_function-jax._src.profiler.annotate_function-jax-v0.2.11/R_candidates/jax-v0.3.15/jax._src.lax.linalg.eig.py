@_warn_on_positional_kwargs
def eig(x, *, compute_left_eigenvectors=True, compute_right_eigenvectors=True):
  """Eigendecomposition of a general matrix.

  Nonsymmetric eigendecomposition is at present only implemented on CPU.
  """
  return eig_p.bind(x, compute_left_eigenvectors=compute_left_eigenvectors,
                    compute_right_eigenvectors=compute_right_eigenvectors)
