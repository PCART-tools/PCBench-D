def _eigh_tpu_impl(x, *, lower, sort_eigenvalues):
  *_, m, n = x.shape
  assert m == n, (m, n)

  termination_size = 256

  if m <= termination_size:
    eig_vals, eig_vecs = eigh_jacobi(x, lower=lower,
                                     sort_eigenvalues=sort_eigenvalues)
    return eig_vecs, eig_vals

  def eigh_qdwh(x):
    if len(x.shape) > 2:
      return control_flow.map(eigh_qdwh, x)

    # We should only look at elements from the lower/upper triangle. Reflects
    # that triangle into the other triangle to form a Hermitian matrix.
    if lower:
      mask = jnp.tri(n, k=0, dtype=bool)
    else:
      mask = ufuncs.logical_not(jnp.tri(n, k=-1, dtype=bool))
    if dtypes.issubdtype(x.dtype, jnp.complexfloating):
      re = lax.select(mask, lax.real(x), _T(lax.real(x)))
      if lower:
        im_mask = jnp.tri(n, k=-1, dtype=bool)
      else:
        im_mask = ufuncs.logical_not(jnp.tri(n, k=0, dtype=bool))
      im = lax.select(im_mask, lax.imag(x), jnp.zeros_like(lax.imag(x)))
      im = lax.select(mask, im, -_T(im))
      x = lax.complex(re, im)
    else:
      x = lax.select(mask, x, _T(x))

    return lax_eigh.eigh(x, sort_eigenvalues=sort_eigenvalues,
                         termination_size=termination_size)

  eig_vals, eig_vecs = eigh_qdwh(x)
  return eig_vecs, eig_vals
