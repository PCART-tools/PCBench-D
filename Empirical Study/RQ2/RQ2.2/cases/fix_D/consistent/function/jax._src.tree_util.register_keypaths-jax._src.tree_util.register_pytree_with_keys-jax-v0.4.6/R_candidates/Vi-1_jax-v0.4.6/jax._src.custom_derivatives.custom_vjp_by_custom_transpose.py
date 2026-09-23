def custom_vjp_by_custom_transpose(fun, fwd, bwd):
  fun = custom_jvp(fun)

  @fun.defjvp
  def jvp(primals, tangents):
    outs, residuals = fwd(*primals)
    tan_out_types = tree_map(lambda o: core.get_aval(o).at_least_vspace(), outs)
    tan_fn = custom_transpose(partial(disallow_jvp, out_avals=tan_out_types))
    tan_fn.def_transpose(bwd)
    return outs, tan_fn(tan_out_types, residuals, tangents)

  return fun
