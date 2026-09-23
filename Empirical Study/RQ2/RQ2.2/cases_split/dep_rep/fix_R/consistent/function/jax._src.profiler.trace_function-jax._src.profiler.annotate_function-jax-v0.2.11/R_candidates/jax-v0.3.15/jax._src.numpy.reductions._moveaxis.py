def _moveaxis(a, source: int, destination: int):
  # simplified version of jnp.moveaxis() for local use.
  _check_arraylike("moveaxis", a)
  a = _asarray(a)
  source = _canonicalize_axis(source, np.ndim(a))
  destination = _canonicalize_axis(destination, np.ndim(a))
  perm = [i for i in range(np.ndim(a)) if i != source]
  perm.insert(destination, source)
  return lax.transpose(a, perm)
