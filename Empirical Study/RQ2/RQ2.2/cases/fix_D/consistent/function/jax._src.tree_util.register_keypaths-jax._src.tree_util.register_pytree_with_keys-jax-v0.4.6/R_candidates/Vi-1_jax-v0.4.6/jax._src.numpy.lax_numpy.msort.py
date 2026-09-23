@util._wraps(np.msort)
def msort(a):
  # TODO(jakevdp): remove msort after Feb 2023
  warnings.warn("jnp.msort is deprecated; use jnp.sort(a, axis=0) instead", DeprecationWarning)
  return sort(a, axis=0)
