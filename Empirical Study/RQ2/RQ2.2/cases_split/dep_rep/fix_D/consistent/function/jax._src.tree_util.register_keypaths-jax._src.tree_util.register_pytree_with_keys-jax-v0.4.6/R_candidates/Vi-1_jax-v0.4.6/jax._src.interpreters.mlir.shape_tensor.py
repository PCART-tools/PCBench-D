def shape_tensor(sizes: Sequence[Union[int, ir.RankedTensorType]]
                 ) -> ir.RankedTensorType:
  int1d = aval_to_ir_type(core.ShapedArray((1,), np.int32))
  def lower_dim(d):
    if type(d) is int:
      return ir_constant(np.array([d], np.int32))
    else:
      return hlo.ReshapeOp(int1d, hlo.ConvertOp(aval_to_ir_type(core.ShapedArray((), np.int32)), d))
  d, *ds = map(lower_dim, sizes)
  if not ds:
    return d
  else:
    return hlo.ConcatenateOp([d, *ds], i64_attr(0)).result
