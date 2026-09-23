@implements(scipy.linalg.toeplitz)
def toeplitz(c: ArrayLike, r: ArrayLike | None = None) -> Array:
  if r is None:
    check_arraylike("toeplitz", c)
    r = jnp.conjugate(jnp.asarray(c))
  else:
    check_arraylike("toeplitz", c, r)

  c_arr = jnp.asarray(c).flatten()
  r_arr = jnp.asarray(r).flatten()

  ncols, = c_arr.shape
  nrows, = r_arr.shape

  if ncols == 0 or nrows == 0:
    return jnp.empty((ncols, nrows),
                     dtype=jnp.promote_types(c_arr.dtype, r_arr.dtype))

  nelems = ncols + nrows - 1
  elems = jnp.concatenate((c_arr[::-1], r_arr[1:]))
  patches = lax.conv_general_dilated_patches(
      elems.reshape((1, nelems, 1)),
      (nrows,), (1,), 'VALID', dimension_numbers=('NTC', 'IOT', 'NTC'),
      precision=lax.Precision.HIGHEST)[0]
  return jnp.flip(patches, axis=0)
