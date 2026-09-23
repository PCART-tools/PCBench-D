def hessenberg(a: ArrayLike) -> Tuple[Array, Array]:
  """Reduces a square matrix to upper Hessenberg form.

  Currently implemented on CPU only.

  Args:
    a: A floating point or complex square matrix or batch of matrices.

  Returns:
  A ``(a, taus)`` pair, where the upper triangle and first subdiagonal of ``a``
  contain the upper Hessenberg matrix, and the elements below the first
  subdiagonal contain the Householder reflectors. For each Householder
  reflector ``taus`` contains the scalar factors of the elementary Householder
  reflectors.
  """
  return hessenberg_p.bind(a)
