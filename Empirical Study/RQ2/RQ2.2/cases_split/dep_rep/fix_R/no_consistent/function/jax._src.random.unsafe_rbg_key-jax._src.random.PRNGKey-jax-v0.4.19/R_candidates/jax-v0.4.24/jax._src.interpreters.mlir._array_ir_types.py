def _array_ir_types(aval: core.ShapedArray | core.DShapedArray
                    ) -> Sequence[ir.Type]:
  aval = core.physical_aval(aval)  # type: ignore
  if not core.is_constant_shape(aval.shape):
    return _dynamic_array_ir_types(aval)  # type: ignore
  return (ir.RankedTensorType.get(aval.shape, dtype_to_ir_type(aval.dtype)),)
