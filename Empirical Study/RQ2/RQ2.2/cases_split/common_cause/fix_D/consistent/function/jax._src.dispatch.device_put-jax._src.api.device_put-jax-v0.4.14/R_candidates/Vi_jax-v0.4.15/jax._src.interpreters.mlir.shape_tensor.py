def shape_tensor(sizes: Sequence[int | ir.RankedTensorType]
                 ) -> ir.RankedTensorType:
  int1d = aval_to_ir_type(core.ShapedArray((1,), np.int32))
  i32_type = aval_to_ir_type(core.ShapedArray((), np.int32))
  def lower_dim(d):
    if type(d) is int:
      return ir_constant(np.array([d], np.int32))
    else:
      if d.type != i32_type:
        d = hlo.ConvertOp(i32_type, d)
      return hlo.ReshapeOp(int1d, d).result
  ds = map(lower_dim, sizes)
  if not ds:
    return ir_constant(np.array([], np.int32))
  elif len(ds) == 1:
    return ds[0]
  else:
    return hlo.ConcatenateOp(ds, i64_attr(0)).result
