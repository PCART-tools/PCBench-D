def custom_call(
    call_target_name: str,
    out_types: Sequence[ir.Type],
    operands: Sequence[ir.Value],
    *,
    backend_config: str | dict[str, ir.Attribute] = "",
    has_side_effect: bool = False,
    result_shapes: Sequence[ir.Value] | None = None,
    called_computations: Sequence[str] = (),
    api_version: int = 2,
    extra_attributes: dict[str, ir.Attribute] = {},
) -> ir.Operation:
  """Wraps a hlo.CustomCall.

  Args:
    result_shapes: tensors that represent the result shapes, to be used when
      the results have dynamic shapes. If not-None, its length must match the
      number of the results.
    called_computations: the list of function names called by the custom call.
  """
  if backend_config is None:
    backend_config_attr = ir.StringAttr.get("")
  elif isinstance(backend_config, str):
    backend_config_attr = ir.StringAttr.get(backend_config)
  elif isinstance(backend_config, dict):
    # TODO(necula): it seems that the CustomCallOp constructor requires that
    # backend_config_attr be a string attribute, even though in some cases we
    # need it to be a DictAttr, e.g., for ApproxTopK on TPU.
    # "Verification failed: 'stablehlo.custom_call' op attribute 'backend_config' failed to satisfy constraint: string attribute"
    # To workaround this limitation we first set it to the empty string and we
    # use an unregistered attribute mhlo.backend_config to hold the DictAttr.
    # We must also use api_version=1 to ensure that mhlo.backend_config is
    # handled properly.
    backend_config_attr = ir.StringAttr.get("")
    api_version = 1
  else:
    raise ValueError("custom_call backend_config unexpected type: " + str(backend_config))
  attributes = dict(
      call_target_name=ir.StringAttr.get(call_target_name),
      has_side_effect=ir.BoolAttr.get(has_side_effect),
      backend_config=backend_config_attr,
      api_version=i32_attr(api_version),
      called_computations=ir.ArrayAttr.get([
        ir.FlatSymbolRefAttr.get(name) for name in called_computations]),
  )
  attributes.update(extra_attributes)

  if result_shapes is not None:
    # We add the result_shapes at the end of the operands, and must pass
    # the indices_of_output_operands attribute. This attribute is not yet
    # accepted by the CustomCall constructor, so we use build_generic
    attributes["indices_of_shape_operands"] = ir.DenseIntElementsAttr.get(
        np.asarray(list(range(len(operands), len(operands) + len(result_shapes))),
                   dtype=np.int64))
    operands = list(operands) + list(result_shapes)

  op = hlo.CustomCallOp.build_generic(results=out_types, operands=operands, attributes=attributes)
  if isinstance(backend_config, dict):
    backend_config_attr = ir.DictAttr.get(backend_config)
    op.operation.attributes["mhlo.backend_config"] = backend_config_attr
  return op
