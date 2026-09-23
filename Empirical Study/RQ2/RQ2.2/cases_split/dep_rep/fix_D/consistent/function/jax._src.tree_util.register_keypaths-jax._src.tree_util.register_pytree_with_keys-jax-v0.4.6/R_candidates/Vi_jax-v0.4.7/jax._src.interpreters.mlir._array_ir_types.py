def _array_ir_types(aval: Union[core.ShapedArray, core.DShapedArray]
                    ) -> Sequence[ir.Type]:
  if core.is_opaque_dtype(aval.dtype):
    phys_avals = aval.dtype._rules.physical_avals(aval)
    return tuple(itertools.chain(*map(_array_ir_types, phys_avals)))
  if not core.is_constant_shape(aval.shape):
    return _dynamic_array_ir_types(aval)  # type: ignore
  return (ir.RankedTensorType.get(aval.shape, dtype_to_ir_type(aval.dtype)),)
