def _tridiagonal_solve_jax(dl, d, du, b, **kw):
  """Pure JAX implementation of `tridiagonal_solve`."""
  prepend_zero = lambda x: jnp.append(jnp.zeros([1], dtype=x.dtype), x[:-1])
  fwd1 = lambda tu_, x: x[1] / (x[0] - x[2] * tu_)
  fwd2 = lambda b_, x: (x[0] - x[3] * b_) / (x[1] - x[3] * x[2])
  bwd1 = lambda x_, x: x[0] - x[1] * x_
  double = lambda f, args: (f(*args), f(*args))

  # Forward pass.
  _, tu_ = lax.scan(lambda tu_, x: double(fwd1, (tu_, x)),
                    du[0] / d[0],
                    (d, du, dl),
                    unroll=32)

  _, b_ = lax.scan(lambda b_, x: double(fwd2, (b_, x)),
                   b[0] / d[0],
                   (b, d, prepend_zero(tu_), dl),
                   unroll=32)

  # Backsubstitution.
  _, x_ = lax.scan(lambda x_, x: double(bwd1, (x_, x)),
                   b_[-1],
                   (b_[::-1], tu_[::-1]),
                   unroll=32)

  return x_[::-1]
