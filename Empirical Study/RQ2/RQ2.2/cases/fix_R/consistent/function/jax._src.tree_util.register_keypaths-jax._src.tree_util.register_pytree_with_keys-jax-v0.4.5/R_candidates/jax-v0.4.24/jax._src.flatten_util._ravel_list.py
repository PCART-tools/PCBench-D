def _ravel_list(lst):
  if not lst: return jnp.array([], jnp.float32), lambda _: []
  from_dtypes = tuple(dtypes.dtype(l) for l in lst)
  to_dtype = dtypes.result_type(*from_dtypes)
  sizes, shapes = unzip2((jnp.size(x), jnp.shape(x)) for x in lst)
  indices = tuple(np.cumsum(sizes))

  if all(dt == to_dtype for dt in from_dtypes):
    # Skip any dtype conversion, resulting in a dtype-polymorphic `unravel`.
    # See https://github.com/google/jax/issues/7809.
    del from_dtypes, to_dtype
    raveled = jnp.concatenate([jnp.ravel(e) for e in lst])
    return raveled, HashablePartial(_unravel_list_single_dtype, indices, shapes)

  # When there is more than one distinct input dtype, we perform type
  # conversions and produce a dtype-specific unravel function.
  ravel = lambda e: jnp.ravel(lax.convert_element_type(e, to_dtype))
  raveled = jnp.concatenate([ravel(e) for e in lst])
  unrav = HashablePartial(_unravel_list, indices, shapes, from_dtypes, to_dtype)
  return raveled, unrav
