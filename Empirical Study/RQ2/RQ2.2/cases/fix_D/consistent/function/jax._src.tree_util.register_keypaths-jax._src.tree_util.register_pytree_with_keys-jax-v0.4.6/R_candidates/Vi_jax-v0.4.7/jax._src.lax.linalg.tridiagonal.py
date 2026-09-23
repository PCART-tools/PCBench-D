def tridiagonal(a: ArrayLike, *, lower=True
               ) -> Tuple[Array, Array, Array, Array]:
  """Reduces a symmetric/Hermitian matrix to tridiagonal form.

  Currently implemented on CPU and GPU only.

  Args:
    a: A floating point or complex matrix or batch of matrices.
    lower: Describes which triangle of the input matrices to use.
      The other triangle is ignored and not accessed.

  Returns:
  A ``(a, d, e, taus)`` pair. If ``lower=True``, the diagonal and first subdiagonal of
  matrix (or batch of matrices) ``a`` contain the tridiagonal representation,
  and elements below the first subdiagonal contain the elementary Householder
  reflectors, where additionally ``d`` contains the diagonal of the matrix and ``e`` contains
  the first subdiagonal.If ``lower=False`` the diagonal and first superdiagonal of the
  matrix contains the tridiagonal representation, and elements above the first
  superdiagonal contain the elementary Householder reflectors, where
  additionally ``d`` contains the diagonal of the matrix and ``e`` contains the
  first superdiagonal. ``taus`` contains the scalar factors of the elementary
  Householder reflectors.
  """
  arr, d, e, taus, info = tridiagonal_p.bind(jnp.asarray(a), lower=lower)
  nan = arr.dtype.type(jnp.nan)
  if jnp.issubdtype(arr.dtype, np.complexfloating):
    nan = nan + arr.dtype.type(jnp.nan * 1j)
  arr = jnp.where((info == 0)[..., None, None], arr, nan)
  real_type = jnp.finfo(arr.dtype).dtype.type
  d = jnp.where((info == 0)[..., None], d, real_type(jnp.nan))
  e = jnp.where((info == 0)[..., None], e, real_type(jnp.nan))
  taus = jnp.where((info == 0)[..., None], taus, nan)
  return arr, d, e, taus
