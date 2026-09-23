def gmres(A, b, x0=None, *, tol=1e-5, atol=0.0, restart=20, maxiter=None,
          M=None, solve_method='batched'):
  """
  GMRES solves the linear system A x = b for x, given A and b.

  A is specified as a function performing A(vi) -> vf = A @ vi, and in principle
  need not have any particular special properties, such as symmetry. However,
  convergence is often slow for nearly symmetric operators.

  Parameters
  ----------
  A: ndarray, function, or matmul-compatible object
      2D array or function that calculates the linear map (matrix-vector
      product) ``Ax`` when called like ``A(x)`` or ``A @ x``. ``A``
      must return array(s) with the same structure and shape as its argument.
  b : array or tree of arrays
      Right hand side of the linear system representing a single vector. Can be
      stored as an array or Python container of array(s) with any shape.

  Returns
  -------
  x : array or tree of arrays
      The converged solution. Has the same structure as ``b``.
  info : None
      Placeholder for convergence information. In the future, JAX will report
      the number of iterations when convergence is not achieved, like SciPy.

  Other Parameters
  ----------------
  x0 : array or tree of arrays, optional
      Starting guess for the solution. Must have the same structure as ``b``.
      If this is unspecified, zeroes are used.
  tol, atol : float, optional
      Tolerances for convergence, ``norm(residual) <= max(tol*norm(b), atol)``.
      We do not implement SciPy's "legacy" behavior, so JAX's tolerance will
      differ from SciPy unless you explicitly pass ``atol`` to SciPy's ``gmres``.
  restart : integer, optional
      Size of the Krylov subspace ("number of iterations") built between
      restarts. GMRES works by approximating the true solution x as its
      projection into a Krylov space of this dimension - this parameter
      therefore bounds the maximum accuracy achievable from any guess
      solution. Larger values increase both number of iterations and iteration
      cost, but may be necessary for convergence. The algorithm terminates
      early if convergence is achieved before the full subspace is built.
      Default is 20.
  maxiter : integer
      Maximum number of times to rebuild the size-``restart`` Krylov space
      starting from the solution found at the last iteration. If GMRES
      halts or is very slow, decreasing this parameter may help.
      Default is infinite.
  M : ndarray, function, or matmul-compatible object
      Preconditioner for A.  The preconditioner should approximate the
      inverse of A.  Effective preconditioning dramatically improves the
      rate of convergence, which implies that fewer iterations are needed
      to reach a given error tolerance.
  solve_method : 'incremental' or 'batched'
      The 'incremental' solve method builds a QR decomposition for the Krylov
      subspace incrementally during the GMRES process using Givens rotations.
      This improves numerical stability and gives a free estimate of the
      residual norm that allows for early termination within a single "restart".
      In contrast, the 'batched' solve method solves the least squares problem
      from scratch at the end of each GMRES iteration. It does not allow for
      early termination, but has much less overhead on GPUs.

  See also
  --------
  scipy.sparse.linalg.gmres
  jax.lax.custom_linear_solve
  """

  if x0 is None:
    x0 = tree_map(jnp.zeros_like, b)
  if M is None:
    M = _identity
  A = _normalize_matvec(A)
  M = _normalize_matvec(M)

  b, x0 = device_put((b, x0))
  size = sum(bi.size for bi in tree_leaves(b))

  if maxiter is None:
    maxiter = 10 * size  # copied from scipy
  restart = min(restart, size)

  if tree_structure(x0) != tree_structure(b):
    raise ValueError(
        'x0 and b must have matching tree structure: '
        f'{tree_structure(x0)} vs {tree_structure(b)}')

  b_norm = _norm(b)
  atol = jnp.maximum(tol * b_norm, atol)

  Mb = M(b)
  Mb_norm = _norm(Mb)
  ptol = Mb_norm * jnp.minimum(1.0, atol / b_norm)

  if solve_method == 'incremental':
    gmres_func = _gmres_incremental
  elif solve_method == 'batched':
    gmres_func = _gmres_batched
  else:
    raise ValueError(f"invalid solve_method {solve_method}, must be either "
                     "'incremental' or 'batched'")

  def _solve(A, b):
    return _gmres_solve(A, b, x0, atol, ptol, restart, maxiter, M, gmres_func)
  x = lax.custom_linear_solve(A, b, solve=_solve, transpose_solve=_solve)

  failed = jnp.isnan(_norm(x))
  info = jnp.where(failed, x=-1, y=0)
  return x, info
