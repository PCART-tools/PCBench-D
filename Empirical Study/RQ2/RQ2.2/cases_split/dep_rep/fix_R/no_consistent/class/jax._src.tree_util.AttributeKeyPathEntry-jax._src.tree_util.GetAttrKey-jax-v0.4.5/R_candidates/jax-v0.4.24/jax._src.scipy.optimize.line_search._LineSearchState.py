class _LineSearchState(NamedTuple):
  done: bool | jax.Array
  failed: bool | jax.Array
  i: int | jax.Array
  a_i1: float | jax.Array
  phi_i1: float | jax.Array
  dphi_i1: float | jax.Array
  nfev: int | jax.Array
  ngev: int | jax.Array
  a_star: float | jax.Array
  phi_star: float | jax.Array
  dphi_star: float | jax.Array
  g_star: jax.Array
