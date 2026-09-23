class _LineSearchResults(NamedTuple):
  """Results of line search.

  Parameters:
    failed: True if the strong Wolfe criteria were satisfied
    nit: integer number of iterations
    nfev: integer number of functions evaluations
    ngev: integer number of gradients evaluations
    k: integer number of iterations
    a_k: integer step size
    f_k: final function value
    g_k: final gradient value
    status: integer end status
  """
  failed: Union[bool, jnp.ndarray]
  nit: Union[int, jnp.ndarray]
  nfev: Union[int, jnp.ndarray]
  ngev: Union[int, jnp.ndarray]
  k: Union[int, jnp.ndarray]
  a_k: Union[int, jnp.ndarray]
  f_k: jnp.ndarray
  g_k: jnp.ndarray
  status: Union[bool, jnp.ndarray]
