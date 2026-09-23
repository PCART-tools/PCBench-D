class OptimizeResults(NamedTuple):
  """Object holding optimization results.

  Parameters:
    x: final solution.
    success: ``True`` if optimization succeeded.
    status: integer solver specific return code. 0 means converged (nominal),
      1=max BFGS iters reached, 3=zoom failed, 4=saddle point reached,
      5=max line search iters reached, -1=undefined
    fun: final function value.
    jac: final jacobian array.
    hess_inv: final inverse Hessian estimate.
    nfev: integer number of function calls used.
    njev: integer number of gradient evaluations.
    nit: integer number of iterations of the optimization algorithm.
  """
  x: jnp.ndarray
  success: Union[bool, jnp.ndarray]
  status: Union[int, jnp.ndarray]
  fun: jnp.ndarray
  jac: jnp.ndarray
  hess_inv: Optional[jnp.ndarray]
  nfev: Union[int, jnp.ndarray]
  njev: Union[int, jnp.ndarray]
  nit: Union[int, jnp.ndarray]
