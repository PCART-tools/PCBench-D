def _wrap_with_spmd_op(name: str,
                       ctx: LoweringRuleContext,
                       x: ir.Value,
                       aval_out: core.AbstractValue,
                       sharding_proto: xc.OpSharding,
                       unspecified_dims: set[int] | None = None):
  # unspecified_dims indicate dimensions whose shardings are not specified and
  # XLA sharding propagation can change them.
  if unspecified_dims:
    backend_config = "unspecified_dims=[" + ",".join(
        [str(i) for i in sorted(unspecified_dims)]) + "]"
  else:
    backend_config = ""
  result_type = aval_to_ir_type(aval_out)
  out_shape = core.physical_aval(aval_out).shape  # type: ignore
  if core.is_constant_shape(out_shape):
    result_shapes = None
  else:
    result_shapes = [eval_dynamic_shape_as_tensor(ctx, out_shape)]

  op = custom_call(name, [result_type], [x],
                   backend_config=backend_config,
                   has_side_effect=False,
                   api_version=1,
                   result_shapes=result_shapes)
  set_sharding(op, sharding_proto)
  return op.result
