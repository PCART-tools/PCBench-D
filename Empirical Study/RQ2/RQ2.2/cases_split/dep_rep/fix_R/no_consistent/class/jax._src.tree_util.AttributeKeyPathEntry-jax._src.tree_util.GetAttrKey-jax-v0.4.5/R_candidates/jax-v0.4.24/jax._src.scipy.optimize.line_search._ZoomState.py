class _ZoomState(NamedTuple):
  done: bool | jax.Array
  failed: bool | jax.Array
  j: int | jax.Array
  a_lo: float | jax.Array
  phi_lo: float | jax.Array
  dphi_lo: float | jax.Array
  a_hi: float | jax.Array
  phi_hi: float | jax.Array
  dphi_hi: float | jax.Array
  a_rec: float | jax.Array
  phi_rec: float | jax.Array
  a_star: float | jax.Array
  phi_star: float | jax.Array
  dphi_star: float | jax.Array
  g_star: float | jax.Array
  nfev: int | jax.Array
  ngev: int | jax.Array
