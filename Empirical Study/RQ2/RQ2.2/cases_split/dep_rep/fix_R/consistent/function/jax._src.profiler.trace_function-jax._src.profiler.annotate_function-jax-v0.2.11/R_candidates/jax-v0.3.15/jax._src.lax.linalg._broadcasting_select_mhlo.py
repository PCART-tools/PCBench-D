def _broadcasting_select_mhlo(which, x, y):
  """Wrapper around XLA `Select` that broadcasts its arguments."""
  which_type, x_type, y_type = (
    ir.RankedTensorType(v.type) for v in (which, x, y))
  out_shape = list(lax_internal.broadcast_shapes(
      tuple(which_type.shape), tuple(x_type.shape), tuple(y_type.shape)))
  bcast_dims = lambda shape: mlir.dense_int_elements(
      range(len(out_shape) - len(shape), len(out_shape)))
  if which_type.shape != out_shape:
    which = mhlo.BroadcastInDimOp(
        ir.RankedTensorType.get(out_shape, which_type.element_type), which,
        bcast_dims(which_type.shape))
  if x_type.shape != out_shape:
    x = mhlo.BroadcastInDimOp(
        ir.RankedTensorType.get(out_shape, x_type.element_type), x,
        bcast_dims(x_type.shape))
  if y_type.shape != out_shape:
    y = mhlo.BroadcastInDimOp(
        ir.RankedTensorType.get(out_shape, y_type.element_type), y,
        bcast_dims(y_type.shape))
  return mhlo.SelectOp(which, x, y).result
