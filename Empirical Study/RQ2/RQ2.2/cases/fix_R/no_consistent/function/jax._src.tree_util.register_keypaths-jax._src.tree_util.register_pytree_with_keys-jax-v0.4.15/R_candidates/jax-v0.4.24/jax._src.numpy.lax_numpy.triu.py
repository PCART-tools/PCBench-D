@util.implements(np.triu, update_doc=False)
@partial(jit, static_argnames=('k',))
def triu(m: ArrayLike, k: int = 0) -> Array:
  util.check_arraylike("triu", m)
  m_shape = shape(m)
  if len(m_shape) < 2:
    raise ValueError("Argument to jax.numpy.triu must be at least 2D")
  N, M = m_shape[-2:]
  mask = tri(N, M, k=k - 1, dtype=bool)
  return lax.select(lax.broadcast(mask, m_shape[:-2]), zeros_like(m), m)
