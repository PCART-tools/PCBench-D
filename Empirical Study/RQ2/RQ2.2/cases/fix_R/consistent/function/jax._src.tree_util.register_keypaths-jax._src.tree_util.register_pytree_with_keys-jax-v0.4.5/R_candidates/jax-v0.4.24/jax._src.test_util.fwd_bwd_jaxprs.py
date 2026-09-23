def fwd_bwd_jaxprs(f, *example_args):
  fwd_jaxpr, (y_shape, res_shape) = jax.make_jaxpr(
      lambda *args: jax.vjp(f, *args), return_shape=True)(*example_args)
  bwd_jaxpr = jax.make_jaxpr(lambda res, outs: res(outs))(res_shape, y_shape)
  return fwd_jaxpr, bwd_jaxpr
