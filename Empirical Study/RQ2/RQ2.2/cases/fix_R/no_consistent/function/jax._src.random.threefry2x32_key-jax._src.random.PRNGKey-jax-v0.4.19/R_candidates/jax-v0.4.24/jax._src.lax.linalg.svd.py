@_warn_on_positional_kwargs
def svd(x: ArrayLike, *, full_matrices: bool = True, compute_uv: bool = True) -> Array | tuple[Array, Array, Array]:
  """Singular value decomposition.

  Returns the singular values if compute_uv is False, otherwise returns a triple
  containing the left singular vectors, the singular values and the adjoint of
  the right singular vectors.
  """
  result = svd_p.bind(x, full_matrices=full_matrices, compute_uv=compute_uv)
  if compute_uv:
    s, u, v = result
    return u, s, v
  else:
    s, = result
    return s
