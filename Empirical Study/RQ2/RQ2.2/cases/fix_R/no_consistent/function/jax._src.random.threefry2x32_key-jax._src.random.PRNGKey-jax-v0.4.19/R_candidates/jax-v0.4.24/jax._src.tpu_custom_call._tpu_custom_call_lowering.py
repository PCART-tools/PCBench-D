def _tpu_custom_call_lowering(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,  # pylint: disable=missing-function-docstring
    config: CustomCallBackendConfig,
    kernel_name: str | None,
    kernel_regeneration_metadata: bytes | None,
    out_avals: Any,
    input_output_aliases: tuple[tuple[int, int], ...],
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
    if axis_context.num_devices != 1:
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
      output_operand_aliases=ir.ArrayAttr.get([
          hlo.OutputOperandAlias.get(
              # if len(result_types) == 1 then the aliasing refers implicitly to
              # the only output.
              output_tuple_indices=[output_idx]
              if len(out_avals) > 1
              else [],
              operand_index=input_idx,
              operand_tuple_indices=[],
          )
          for input_idx, output_idx in input_output_aliases
      ]),
  )

  # Add kernel_name and kernel_regeneration_metadata as attributes to the
  # custom call op. This is because we do not want to pollute the backend_config
  # with this information.
  if kernel_name is not None:
    call.attributes["kernel_name"] = ir.StringAttr.get(kernel_name)
  if kernel_regeneration_metadata is not None:
    call.attributes["kernel_regeneration_metadata"] = ir.StringAttr.get(
        base64.b64encode(kernel_regeneration_metadata)
    )
  if multiple_results:
    results = [stablehlo.get_tuple_element(call, mlir.i32_attr(i))
               for i in range(len(out_avals))]
  else:
    results = call.results
  return results
