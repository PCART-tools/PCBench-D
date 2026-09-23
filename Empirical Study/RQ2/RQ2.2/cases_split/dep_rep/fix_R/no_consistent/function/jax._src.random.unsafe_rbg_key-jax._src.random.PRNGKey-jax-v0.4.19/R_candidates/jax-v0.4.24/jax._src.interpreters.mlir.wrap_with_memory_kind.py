def wrap_with_memory_kind(
    x: ir.Value, memory_kind: str, aval_out: core.AbstractValue,
    is_input: bool = False) -> ir.Value:
  if aval_out is None:
    result_type = x.type
  else:
    result_type = aval_to_ir_type(aval_out)
  op = custom_call("annotate_device_placement", result_types=[result_type],
                   operands=[x], api_version=1)
  mka = get_compute_type(memory_kind)
  dict_attr = {"_xla_compute_type": ir.StringAttr.get(mka)}
  if is_input and mka == 'host':
    dict_attr.update({"_xla_buffer_placement": ir.StringAttr.get("arg")})
  op.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get(dict_attr)
  return op.result
