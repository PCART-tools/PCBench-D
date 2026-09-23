def _qdwh(x, m, n, is_hermitian, max_iterations, eps):
  """QR-based dynamically weighted Halley iteration for polar decomposition."""

  # Estimates `alpha` and `beta = alpha * l`, where `alpha` is an estimate of
  # norm(x, 2) such that `alpha >= norm(x, 2)` and `beta` is a lower bound for
  # the smallest singular value of x.
  if eps is None:
    eps = float(jnp.finfo(x.dtype).eps)
  alpha = (jnp.sqrt(jnp.linalg.norm(x, ord=1)) *
           jnp.sqrt(jnp.linalg.norm(x, ord=jnp.inf))).astype(x.dtype)
  l = eps

  u = x / alpha

  # Iteration tolerances.
  tol_l = 10.0 * eps / 2.0
  tol_norm = jnp.cbrt(tol_l)

  def cond_fun(state):
    _, _, _, is_unconverged, is_not_max_iteration = state
    return jnp.logical_and(is_unconverged, is_not_max_iteration)

  def body_fun(state):
    u, l, iter_idx, _, _ = state

    u_prev = u

    # Computes parameters.
    l2 = l**2
    dd = jnp.cbrt(4.0 * (1.0 / l2 - 1.0) / l2)
    sqd = jnp.sqrt(1.0 + dd)
    a = (sqd + jnp.sqrt(8.0 - 4.0 * dd + 8.0 * (2.0 - l2) / (l2 * sqd)) / 2)
    a = jnp.real(a)
    b = (a - 1.0)**2 / 4.0
    c = a + b - 1.0

    # Updates l.
    l = l * (a + b * l2) / (1.0 + c * l2)

    # Uses QR or Cholesky decomposition.
    def true_fn(u):
      return _use_qr(u, m, n, params=(a, b, c))

    def false_fn(u):
      return _use_cholesky(u, m, n, params=(a, b, c))

    u = jax.lax.cond(c > 100, true_fn, false_fn, operand=(u))

    if is_hermitian:
      u = (u + u.T.conj()) / 2.0

    # Checks convergence.
    iterating_l = jnp.abs(1.0 - l) > tol_l
    iterating_u = jnp.linalg.norm(u-u_prev) > tol_norm
    is_unconverged = jnp.logical_or(iterating_l, iterating_u)

    is_not_max_iteration = iter_idx < max_iterations

    return u, l, iter_idx + 1, is_unconverged, is_not_max_iteration

  iter_idx = 1
  is_unconverged = True
  is_not_max_iteration = True
  u, _, num_iters, is_unconverged, _ = jax.lax.while_loop(
      cond_fun=cond_fun, body_fun=body_fun,
      init_val=(u, l, iter_idx, is_unconverged, is_not_max_iteration))

  # Applies Newton-Schulz refinement for better accuracy.
  u = 1.5 * u - 0.5 * u @ (u.T.conj() @ u)

  h = u.T.conj() @ x
  h = (h + h.T.conj()) / 2.0

  # Converged within the maximum number of iterations.
  is_converged = jnp.logical_not(is_unconverged)

  return u, h, num_iters - 1, is_converged
