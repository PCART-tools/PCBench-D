class _BFGSResults(NamedTuple):
  """Results from BFGS optimization.

  Parameters:
    converged: True if minimization converged.
    failed: True if line search failed.
    k: integer the number of iterations of the BFGS update.
    nfev: integer total number of objective evaluations performed.
    ngev: integer total number of jacobian evaluations
    nhev: integer total number of hessian evaluations
    x_k: array containing the last argument value found during the search. If
      the search converged, then this value is the argmin of the objective
      function.
    f_k: array containing the value of the objective function at `x_k`. If the
      search converged, then this is the (local) minimum of the objective
      function.
    g_k: array containing the gradient of the objective function at `x_k`. If
      the search converged the l2-norm of this tensor should be below the
      tolerance.
    H_k: array containing the inverse of the estimated Hessian.
    status: int describing end state.
    line_search_status: int describing line search end state (only means
      something if line search fails).
  """
  converged: Union[bool, jnp.ndarray]
  failed: Union[bool, jnp.ndarray]
  k: Union[int, jnp.ndarray]
  nfev: Union[int, jnp.ndarray]
  ngev: Union[int, jnp.ndarray]
  nhev: Union[int, jnp.ndarray]
  x_k: jnp.ndarray
  f_k: jnp.ndarray
  g_k: jnp.ndarray
  H_k: jnp.ndarray
  old_old_fval: jnp.ndarray
  status: Union[int, jnp.ndarray]
  line_search_status: Union[int, jnp.ndarray]
