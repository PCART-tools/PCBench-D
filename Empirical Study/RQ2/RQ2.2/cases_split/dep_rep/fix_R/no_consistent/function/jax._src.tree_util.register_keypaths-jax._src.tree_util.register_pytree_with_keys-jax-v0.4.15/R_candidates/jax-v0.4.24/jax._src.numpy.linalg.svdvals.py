@implements(getattr(np.linalg, "svdvals", None))
def svdvals(x: ArrayLike, /) -> Array:
  check_arraylike('jnp.linalg.svdvals', x)
  return svd(x, compute_uv=False, hermitian=False)
