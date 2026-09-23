def _wrap_with_spmd_op(name: str,
                       result_type: ir.Type,
                       x: ir.Value,
                       sharding_proto: xc.OpSharding,
                       unspecified_dims: Optional[Set[int]] = None):
  # unspecified_dims indicate dimensions whose shardings are not specified and
  # XLA sharding propagation can change them.
  if unspecified_dims:
    backend_config = "unspecified_dims=[" + ",".join(
        [str(i) for i in sorted(unspecified_dims)]) + "]"
  else:
    backend_config = ""
  op = hlo.CustomCallOp([result_type], [x],
                        call_target_name=ir.StringAttr.get(name),
                        has_side_effect=ir.BoolAttr.get(False),
                        backend_config=ir.StringAttr.get(backend_config),
                        api_version=i32_attr(1),
                        called_computations=ir.ArrayAttr.get([]),
                        operand_layouts=None,
                        result_layouts=None)
  set_sharding(op, sharding_proto)
  return op.result
