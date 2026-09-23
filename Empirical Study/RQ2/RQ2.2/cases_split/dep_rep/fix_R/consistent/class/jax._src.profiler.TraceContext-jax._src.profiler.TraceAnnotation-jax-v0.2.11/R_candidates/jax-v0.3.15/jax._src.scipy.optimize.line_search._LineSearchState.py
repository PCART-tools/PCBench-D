class _LineSearchState(NamedTuple):
  done: Union[bool, jnp.ndarray]
  failed: Union[bool, jnp.ndarray]
  i: Union[int, jnp.ndarray]
  a_i1: Union[float, jnp.ndarray]
  phi_i1: Union[float, jnp.ndarray]
  dphi_i1: Union[float, jnp.ndarray]
  nfev: Union[int, jnp.ndarray]
  ngev: Union[int, jnp.ndarray]
  a_star: Union[float, jnp.ndarray]
  phi_star: Union[float, jnp.ndarray]
  dphi_star: Union[float, jnp.ndarray]
  g_star: jnp.ndarray
