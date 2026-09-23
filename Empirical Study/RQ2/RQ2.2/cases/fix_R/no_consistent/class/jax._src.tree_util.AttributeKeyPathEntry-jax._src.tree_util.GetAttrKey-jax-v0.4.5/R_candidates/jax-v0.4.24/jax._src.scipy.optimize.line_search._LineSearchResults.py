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
  failed: bool | jax.Array
  nit: int | jax.Array
  nfev: int | jax.Array
  ngev: int | jax.Array
  k: int | jax.Array
  a_k: int | jax.Array
  f_k: jax.Array
  g_k: jax.Array
  status: bool | jax.Array
