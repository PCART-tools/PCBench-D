@util._wraps(np.tril_indices)
def tril_indices(n: int, k: int = 0, m: Optional[int] = None) -> tuple[Array, Array]:
  n = core.concrete_or_error(operator.index, n, "n argument of jnp.triu_indices")
  k = core.concrete_or_error(operator.index, k, "k argument of jnp.triu_indices")
  m = n if m is None else core.concrete_or_error(operator.index, m, "m argument of jnp.triu_indices")
  i, j = nonzero(tril(ones((n, m)), k=k), size=_triu_size(m, n, -k))
  return i, j
