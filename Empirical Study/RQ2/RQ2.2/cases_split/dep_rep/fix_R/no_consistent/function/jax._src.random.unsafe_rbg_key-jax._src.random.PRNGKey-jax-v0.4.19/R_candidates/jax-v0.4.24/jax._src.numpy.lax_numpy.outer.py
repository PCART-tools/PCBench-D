@util.implements(np.outer, skip_params=['out'])
@partial(jit, inline=True)
def outer(a: ArrayLike, b: ArrayLike, out: None = None) -> Array:
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.outer is not supported.")
  # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
  util.check_arraylike("outer", a, b, emit_warning=True)
  a, b = util.promote_dtypes(a, b)
  return ravel(a)[:, None] * ravel(b)[None, :]
