def _moveaxis(a: ArrayLike, source: int, destination: int) -> Array:
  # simplified version of jnp.moveaxis() for local use.
  check_arraylike("moveaxis", a)
  a = lax_internal.asarray(a)
  source = _canonicalize_axis(source, np.ndim(a))
  destination = _canonicalize_axis(destination, np.ndim(a))
  perm = [i for i in range(np.ndim(a)) if i != source]
  perm.insert(destination, source)
  return lax.transpose(a, perm)
