@util._wraps(np.outer, skip_params=['out'])
@partial(jit, inline=True)
def outer(a, b, out=None):
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.outer is not supported.")
  a, b = util.promote_dtypes(a, b)
  return ravel(a)[:, None] * ravel(b)[None, :]
