def eig_lower(*args, **kw):
  raise NotImplementedError(
    "Nonsymmetric eigendecomposition is only implemented on the CPU backend. "
    "If your matrix is symmetric or Hermitian, you should use eigh instead.")
