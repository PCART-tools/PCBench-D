@_warn_on_positional_kwargs
def eigh(
    x: Array,
    *,
    lower: bool = True,
    symmetrize_input: bool = True,
    sort_eigenvalues: bool = True,
    subset_by_index: tuple[int, int] | None = None,
) -> tuple[Array, Array]:
  r"""Eigendecomposition of a Hermitian matrix.

  Computes the eigenvectors and eigenvalues of a complex Hermitian or real
  symmetric square matrix.

  Args:
    x: A batch of square complex Hermitian or real symmetric matrices with shape
      ``[..., n, n]``.
    lower: If ``symmetrize_input`` is ``False``, describes which triangle of the
      input matrix to use. If ``symmetrize_input`` is ``False``, only the
      triangle given by ``lower`` is accessed; the other triangle is ignored and
      not accessed.
    symmetrize_input: If ``True``, the matrix is symmetrized before the
      eigendecomposition by computing :math:`\frac{1}{2}(x + x^H)`.
    sort_eigenvalues: If ``True``, the eigenvalues will be sorted in ascending
      order. If ``False`` the eigenvalues are returned in an
      implementation-defined order.
     subset_by_index: Optional 2-tuple [start, end] indicating the range of
       indices of eigenvalues to compute. For example, is ``range_select`` =
       [n-2,n], then ``eigh`` computes the two largest eigenvalues and their
       eigenvectors.

  Returns:
    A tuple ``(v, w)``.

    ``v`` is an array with the same dtype as ``x`` such that ``v[..., :, i]`` is
    the normalized eigenvector corresponding to eigenvalue ``w[..., i]``.

    ``w`` is an array with the same dtype as ``x`` (or its real counterpart if
    complex) with shape ``[..., d]`` containing the eigenvalues of ``x`` in
    ascending order(each repeated according to its multiplicity).
    If ``subset_by_index`` is ``None`` then ``d`` is equal to ``n``. Otherwise
    ``d`` is equal to ``subset_by_index[1] - subset_by_index[0]``.
  """
  if symmetrize_input:
    x = symmetrize(x)
  v, w = eigh_p.bind(
      x,
      lower=lower,
      sort_eigenvalues=sort_eigenvalues,
      subset_by_index=subset_by_index,
  )
  return v, w
