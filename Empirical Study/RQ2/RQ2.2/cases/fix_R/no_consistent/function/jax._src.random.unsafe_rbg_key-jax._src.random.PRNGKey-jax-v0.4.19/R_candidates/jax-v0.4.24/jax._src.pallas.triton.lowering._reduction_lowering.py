def _reduction_lowering(body, ctx: TritonLoweringRuleContext, a, axes):
  flat_args = tree_util.tree_leaves(a)
  (axis,) = axes
  mapped_avals = [jax_core.ShapedArray((), aval.dtype) for aval in ctx.avals_in]
  in_tree = tree_util.tree_structure((a, a))
  flat_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
      lu.wrap_init(body), in_tree
  )
  combine_jaxpr, _, consts, () = pe.trace_to_jaxpr_dynamic(
      flat_fun, [*mapped_avals, *mapped_avals]
  )
  out_tree = out_tree_thunk()
  del out_tree  # Not needed
  if consts:
    raise NotImplementedError("Reductions with constants not supported.")
  element_types = [arg.type.scalar for arg in flat_args]
  reduce_op = tt_dialect.ReduceOp([t.handle for t in flat_args], axis)
  param_types = element_types * 2
  ir_param_types = [ty.to_ir(ctx.builder) for ty in param_types]
  entry = reduce_op.regions[0].blocks.append(*ir_param_types)
  combine_args = [
      tc.tensor(entry.arguments[i], ty) for i, ty in enumerate(param_types)
  ]
  with ir.InsertionPoint.at_block_begin(entry):
    results = lower_jaxpr_to_triton_ir(
        ctx.context, combine_jaxpr, None, *combine_args
    )
    tt_dialect.reduce_return([r.handle for r in results])
  reduce_op.verify()

  def wrap_tensor(x, scalar_ty):
    if ctx.avals_out[0].shape:
      res_ty = tc.block_type(scalar_ty, ctx.avals_out[0].shape)
    else:
      # 0d-tensor -> scalar
      res_ty = scalar_ty
    return tc.tensor(x, res_ty)

  return map(wrap_tensor, reduce_op.result, element_types)
