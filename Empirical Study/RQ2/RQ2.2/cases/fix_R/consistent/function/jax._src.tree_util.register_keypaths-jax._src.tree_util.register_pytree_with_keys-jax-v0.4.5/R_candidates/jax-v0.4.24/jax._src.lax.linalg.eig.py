@_warn_on_positional_kwargs
def eig(x: ArrayLike, *, compute_left_eigenvectors: bool = True,
        compute_right_eigenvectors: bool = True) -> list[Array]:
  """Eigendecomposition of a general matrix.

  Nonsymmetric eigendecomposition is at present only implemented on CPU.

  Args:
    x: A batch of square matrices with shape ``[..., n, n]``.
    compute_left_eigenvectors: If true, the left eigenvectors will be computed.
    compute_right_eigenvectors: If true, the right eigenvectors will be
      computed.
  Returns:
    The eigendecomposition of ``x``, which is a tuple of the form
    ``(w, vl, vr)`` where ``w`` are the eigenvalues, ``vl`` are the left
    eigenvectors, and ``vr`` are the right eigenvectors. ``vl`` and ``vr`` are
    optional and will only be included if ``compute_left_eigenvectors`` or
    ``compute_right_eigenvectors`` respectively are ``True``.

    If the eigendecomposition fails, then arrays full of NaNs will be returned
    for that batch element.
  """
  return eig_p.bind(x, compute_left_eigenvectors=compute_left_eigenvectors,
                    compute_right_eigenvectors=compute_right_eigenvectors)
