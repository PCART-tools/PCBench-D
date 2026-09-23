def _tpu_custom_call_lowering(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,  # pylint: disable=missing-function-docstring
    config: CustomCallBackendConfig,
    out_avals: Any,
) -> ...:
  i32_type = ir.IntegerType.get_signless(32)
  multiple_results = len(out_avals) > 1
  if multiple_results:
    result_type = ir.TupleType.get_tuple(
        [mlir.aval_to_ir_type(aval) for aval in out_avals]
    )
  else:
    result_type = mlir.aval_to_ir_type(out_avals[0])
  axis_context = ctx.module_context.axis_context
  sharding_impls = jax._src.sharding_impls  # pylint: disable=protected-access
  if isinstance(axis_context, sharding_impls.SPMDAxisContext):
    if axis_context.manual_axes != frozenset(axis_context.mesh.axis_names):
      raise NotImplementedError(
          "Mosaic kernels cannot be automatically partitioned. Please wrap the"
          " call in a shard_map or xmap."
      )
  elif isinstance(axis_context, sharding_impls.ShardingContext):
    if len(axis_context.device_assignment) != 1:
      raise NotImplementedError(
          "Mosaic kernels cannot be automatically partitioned. Please wrap the"
          " call in a shard_map or xmap."
      )
  elif config.has_communication:
    raise NotImplementedError(
        "Replica lowering for Mosaic kernels not implemented."
    )
  call = stablehlo.CustomCallOp(
      [result_type],
      in_nodes,
      call_target_name=ir.StringAttr.get(b"tpu_custom_call"),
      has_side_effect=ir.BoolAttr.get(False),
      backend_config=ir.StringAttr.get(config.to_json()),
      api_version=ir.IntegerAttr.get(i32_type, 1),
      called_computations=ir.ArrayAttr.get([]),
      operand_layouts=_avals_to_layouts(ctx.avals_in),
      result_layouts=_avals_to_layouts(ctx.avals_out),
      output_operand_aliases=None,
  )
  if multiple_results:
    results = [stablehlo.GetTupleElementOp(call, mlir.i32_attr(i)).result
               for i in range(len(out_avals))]
  else:
    results = call.results
  return results
