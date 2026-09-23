def xla_fallback_lowering(prim: core.Primitive):
  @cache_lowering
  def fallback(ctx: LoweringRuleContext, *args, **params):
    module_ctx = ctx.module_context
    axis_ctx = module_ctx.axis_context
    if isinstance(axis_ctx, sharding_impls.SPMDAxisContext):
      axis_env = axis_ctx.unsafe_axis_env
    else:
      axis_env = module_ctx.axis_env

    if any(hasattr(a, "shape") and
           not core.is_constant_shape(a.shape) for a in (ctx.avals_in + ctx.avals_out)):
      raise NotImplementedError(
          f"Shape polymorphism for xla_fallback_lowering is not implemented ({ctx.primitive}); b/261682623")

    if len(module_ctx.platforms) > 1:
      raise NotImplementedError(
        "fallback lowering not implemented for multi-platform lowering")
    xla_computation = xla.primitive_subcomputation(
        module_ctx.platforms[0], axis_env, prim, ctx.avals_in,
        ctx.avals_out, **params)
    xla_module = xla_computation_to_mlir_module(xla_computation)
    callee_name = merge_mlir_modules(
        module_ctx.module, f"xla_fallback_{prim.name}", xla_module)
    output_types = map(aval_to_ir_types, ctx.avals_out)
    flat_output_types = util.flatten(output_types)
    output_type = (ir.TupleType.get_tuple(flat_output_types)
                   if prim.multiple_results else flat_output_types[0])

    call = func_dialect.CallOp([output_type],
                               ir.FlatSymbolRefAttr.get(callee_name),
                               flatten_lowering_ir_args(args)).result
    if not prim.multiple_results:
      return [call]
    flat_results = [hlo.get_tuple_element(call, i32_attr(i))
                    for i in range(len(flat_output_types))]

    return util.unflatten(flat_results, map(len, output_types))
  return fallback
