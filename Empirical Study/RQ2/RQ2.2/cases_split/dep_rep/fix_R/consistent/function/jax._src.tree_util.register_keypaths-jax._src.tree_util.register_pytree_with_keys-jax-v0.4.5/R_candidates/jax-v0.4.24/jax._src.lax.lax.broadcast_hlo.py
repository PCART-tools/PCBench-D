def broadcast_hlo(
    aval_out: core.ShapedArray, avals: Sequence[core.ShapedArray],
    args: Sequence[ir.Value]) -> Sequence[ir.Value]:
  """Broadcasts HLO values with broadcast-compatible shapes to the same shape.
  """
  out = []
  for aval, arg in zip(avals, args):
    if aval.shape != aval_out.shape:
      assert len(aval.shape) <= len(aval_out.shape), (aval, aval_out)
      dims = mlir.dense_int_array_v6(
          range(len(aval_out.shape) - len(aval.shape), len(aval_out.shape)))
      if any(isinstance(d, ir.Value) for d in aval_out.shape):
        arg = hlo.dynamic_broadcast_in_dim(
            mlir.aval_to_ir_type(aval_out), arg,
            mlir.shape_tensor(aval_out.shape), dims)
      else:
        arg = hlo.broadcast_in_dim(
            mlir.aval_to_ir_type(aval.update(shape=aval_out.shape)), arg,
            dims)
    out.append(arg)
  return out
