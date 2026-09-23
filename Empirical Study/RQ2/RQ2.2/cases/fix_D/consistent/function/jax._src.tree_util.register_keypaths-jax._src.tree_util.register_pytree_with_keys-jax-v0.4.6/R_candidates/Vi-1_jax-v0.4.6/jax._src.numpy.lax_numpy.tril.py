@util._wraps(np.tril)
@partial(jit, static_argnames=('k',))
def tril(m: ArrayLike, k: int = 0) -> Array:
  util._check_arraylike("tril", m)
  m_shape = shape(m)
  if len(m_shape) < 2:
    raise ValueError("Argument to jax.numpy.tril must be at least 2D")
  N, M = m_shape[-2:]
  mask = tri(N, M, k=k, dtype=bool)
  return lax.select(lax.broadcast(mask, m_shape[:-2]), m, zeros_like(m))
