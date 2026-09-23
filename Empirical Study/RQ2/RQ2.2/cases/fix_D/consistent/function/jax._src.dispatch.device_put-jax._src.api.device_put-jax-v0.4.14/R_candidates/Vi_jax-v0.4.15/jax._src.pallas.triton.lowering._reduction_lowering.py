def _reduction_lowering(body, ctx: TritonLoweringRuleContext, args, axes):
  flat_args = tree_util.tree_leaves(args)
  (axis,) = axes
  mapped_avals = [
      jax_core.mapped_aval(aval.shape[axis], axis, aval)
      for aval in ctx.avals_in
  ]
  in_tree = tree_util.tree_structure((args, args))
  flat_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
      lu.wrap_init(body), in_tree
  )
  combine_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      flat_fun, [*mapped_avals, *mapped_avals]
  )
  out_tree = out_tree_thunk()
  del out_tree  # Not needed
  if consts:
    raise NotImplementedError("Reductions with constants not supported.")
  element_types = [arg.type.scalar for arg in flat_args]
  builder = ctx.builder
  reduce_op = builder.create_reduce([t.handle for t in flat_args], axis)
  region = reduce_op.get_region(0)
  old_ip = builder.get_insertion_point()
  param_types = element_types * 2
  ir_param_types = [ty.to_ir(builder) for ty in param_types]
  block = builder.create_block_with_parent(region, ir_param_types)
  combine_args = [
      tl.core.tensor(block.arg(i), ty) for i, ty in enumerate(param_types)
  ]
  results = lower_jaxpr_to_triton_ir(ctx, combine_jaxpr, None, *combine_args)
  handles = [r.handle for r in results]
  builder.create_reduce_ret(*handles)
  builder.restore_insertion_point(old_ip)
  reduce_op.verify()

  def wrap_tensor(x, scalar_ty):
    if ctx.avals_out[0].shape:
      res_ty = tl.block_type(scalar_ty, ctx.avals_out[0].shape)
    else:
      # 0d-tensor -> scalar
      res_ty = scalar_ty
    return tl.core.tensor(x, res_ty)

  results = [
      wrap_tensor(reduce_op.get_result(i), ty)
      for i, ty in enumerate(element_types)
  ]
  return results
