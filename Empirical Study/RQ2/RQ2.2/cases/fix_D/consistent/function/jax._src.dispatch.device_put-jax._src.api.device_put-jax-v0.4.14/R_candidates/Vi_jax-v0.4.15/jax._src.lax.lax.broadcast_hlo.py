def broadcast_hlo(
    aval_out: core.ShapedArray, avals: Sequence[core.ShapedArray],
    args: Sequence[ir.Value]) -> Sequence[ir.Value]:
  """Broadcasts HLO values with broadcast-compatible shapes to the same shape.
  """
  out = []
  for aval, arg in zip(avals, args):
    if aval.shape != aval_out.shape:
      assert len(aval.shape) <= len(aval_out.shape), (aval, aval_out)
      dims = mlir.dense_int_elements(
          range(len(aval_out.shape) - len(aval.shape), len(aval_out.shape)))
      if any(isinstance(d, ir.Value) for d in aval_out.shape):
        arg = hlo.DynamicBroadcastInDimOp(
            mlir.aval_to_ir_type(aval_out), arg,
            mlir.shape_tensor(aval_out.shape), dims).result
      else:
        arg = hlo.BroadcastInDimOp(
            mlir.aval_to_ir_type(aval.update(shape=aval_out.shape)), arg,
            dims).result
    out.append(arg)
  return out
