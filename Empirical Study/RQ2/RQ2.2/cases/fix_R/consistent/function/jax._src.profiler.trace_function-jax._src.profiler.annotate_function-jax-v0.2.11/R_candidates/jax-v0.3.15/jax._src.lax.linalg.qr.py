@_warn_on_positional_kwargs
def qr(x, *, full_matrices: bool = True):
  """QR decomposition.

  Computes the QR decomposition

  .. math::
    A = Q . R

  of matrices :math:`A`, such that :math:`Q` is a unitary (orthogonal) matrix,
  and :math:`R` is an upper-triangular matrix.

  Args:
    x: A batch of matrices with shape ``[..., m, n]``.
    full_matrices: Determines if full or reduced matrices are returned; see
      below.

  Returns:
    A pair of arrays ``(q, r)``.

    Array ``q`` is a unitary (orthogonal) matrix,
    with shape ``[..., m, m]`` if ``full_matrices=True``, or
    ``[..., m, min(m, n)]`` if ``full_matrices=False``.

    Array ``r`` is an upper-triangular matrix with shape ``[..., m, n]`` if
    ``full_matrices=True``, or ``[..., min(m, n), n]`` if
    ``full_matrices=False``.
  """
  q, r = qr_p.bind(x, full_matrices=full_matrices)
  return q, r
