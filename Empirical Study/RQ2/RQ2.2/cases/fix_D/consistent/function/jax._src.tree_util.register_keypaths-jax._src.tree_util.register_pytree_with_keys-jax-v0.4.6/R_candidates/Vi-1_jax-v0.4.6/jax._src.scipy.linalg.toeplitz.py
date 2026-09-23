@_wraps(scipy.linalg.toeplitz)
def toeplitz(c: ArrayLike, r: Optional[ArrayLike] = None) -> Array:
  if r is None:
    _check_arraylike("toeplitz", c)
    r = jnp.conjugate(jnp.asarray(c))
  else:
    _check_arraylike("toeplitz", c, r)

  c = jnp.asarray(c).flatten()
  r = jnp.asarray(r).flatten()

  ncols, = c.shape
  nrows, = r.shape

  if ncols == 0 or nrows == 0:
    return jnp.empty((ncols, nrows), dtype=jnp.promote_types(c.dtype, r.dtype))

  nelems = ncols + nrows - 1
  elems = jnp.concatenate((c[::-1], r[1:]))
  patches = lax.conv_general_dilated_patches(
      elems.reshape((1, nelems, 1)),
      (nrows,), (1,), 'VALID', dimension_numbers=('NTC', 'IOT', 'NTC'),
      precision=lax.Precision.HIGHEST)[0]
  return jnp.flip(patches, axis=0)
