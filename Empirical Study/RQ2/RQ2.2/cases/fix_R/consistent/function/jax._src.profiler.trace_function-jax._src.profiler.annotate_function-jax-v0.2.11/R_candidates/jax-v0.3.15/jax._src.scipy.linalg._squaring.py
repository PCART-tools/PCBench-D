@partial(jit, static_argnums=2)
def _squaring(R, n_squarings, max_squarings):
  # squaring step to undo scaling
  def _squaring_precise(x):
    return _precise_dot(x, x)

  def _identity(x):
    return x

  def _scan_f(c, i):
    return lax.cond(i < n_squarings, _squaring_precise, _identity, c), None
  res, _ = lax.scan(_scan_f, R, jnp.arange(max_squarings, dtype=n_squarings.dtype))

  return res
