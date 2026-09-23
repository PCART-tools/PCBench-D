def call_transpose(primitive, params, call_jaxpr, args, ct, _, reduce_axes):
  if isinstance(call_jaxpr, core.ClosedJaxpr):
    call_jaxpr, consts = call_jaxpr.jaxpr, call_jaxpr.consts
  else:
    consts = ()
  all_args, in_tree_def = tree_flatten((consts, args, ct))
  fun = lu.hashable_partial(lu.wrap_init(backward_pass), call_jaxpr,
                            reduce_axes, False)
  fun, out_tree = flatten_fun_nokwargs(fun, in_tree_def)
  update_params = call_transpose_param_updaters.get(primitive)
  if update_params:
    params = update_params(params, map(is_undefined_primal, args),
                           [type(x) is not Zero for x in ct])
  if config.dynamic_shapes.value:
    # TODO(mattjj,dougalm): handle consts, for now assume just args
    which_lin = [is_undefined_primal(x) for x in args]
    res_invars, _ = partition_list(which_lin, call_jaxpr.invars)
    new_invars = [*res_invars, *call_jaxpr.outvars]
    dbidx_map = {v: core.DBIdx(i) for i, v in enumerate(new_invars)}
    in_type = [(v.aval.update(shape=tuple(dbidx_map.get(d, d) for d in v.aval.shape))
                if type(v.aval) is core.DShapedArray else v.aval, True) for v in new_invars]
    fun = lu.annotate(fun, tuple(in_type))
  out_flat = primitive.bind(fun, *all_args, **params)
  return tree_unflatten(out_tree(), out_flat)
