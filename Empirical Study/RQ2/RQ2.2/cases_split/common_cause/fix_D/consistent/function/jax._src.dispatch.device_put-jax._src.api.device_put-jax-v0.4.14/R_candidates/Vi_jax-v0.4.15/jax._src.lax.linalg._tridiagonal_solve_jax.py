def _tridiagonal_solve_jax(dl, d, du, b, **kw):
  """Pure JAX implementation of `tridiagonal_solve`."""
  def prepend_zero(x):
    return jnp.append(
        jnp.zeros((1,) + x.shape[1:], dtype=x.dtype),
        x[:-1], axis=0)
  fwd1 = lambda tu_, x: x[1] / (x[0] - x[2] * tu_)

  def fwd2(b_, x):
    return (x[0] - x[3][jnp.newaxis, ...] * b_) / (
        x[1] - x[3] * x[2])[jnp.newaxis, ...]

  bwd1 = lambda x_, x: x[0] - x[1][jnp.newaxis, ...] * x_
  double = lambda f, args: (f(*args), f(*args))

  # Move relevant dimensions to the front for the scan.
  dl = jnp.moveaxis(dl, -1, 0)
  d = jnp.moveaxis(d, -1, 0)
  du = jnp.moveaxis(du, -1, 0)
  b = jnp.moveaxis(b, -1, 0)
  b = jnp.moveaxis(b, -1, 0)

  # Forward pass.
  _, tu_ = lax.scan(lambda tu_, x: double(fwd1, (tu_, x)),
                    du[0] / d[0],
                    (d, du, dl),
                    unroll=32)

  _, b_ = lax.scan(lambda b_, x: double(fwd2, (b_, x)),
                   b[0] / d[0:1],
                   (b, d, prepend_zero(tu_), dl),
                   unroll=32)

  # Backsubstitution.
  _, x_ = lax.scan(lambda x_, x: double(bwd1, (x_, x)),
                   b_[-1],
                   (b_[::-1], tu_[::-1]),
                   unroll=32)

  result = x_[::-1]
  result = jnp.moveaxis(result, 0, -1)
  result = jnp.moveaxis(result, 0, -1)
  return result
