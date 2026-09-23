def _pred_bcast_select_mhlo(
    pred_aval: core.ShapedArray, pred: ir.Value, xs: Sequence[ir.Value],
    ys: Sequence[ir.Value], x_y_aval: core.AbstractValue) -> Sequence[ir.Value]:
  if x_y_aval is core.abstract_token:
    x, = xs
    y, = ys
    return [mhlo.AfterAllOp(mlir.aval_to_ir_type(x_y_aval), [x, y]).result]
  else:
    assert isinstance(x_y_aval, core.ShapedArray), x_y_aval
    x, = xs
    y, = ys
    assert x.type == y.type, (x.type, y.type)
    assert (pred_aval.shape == x_y_aval.shape[:len(pred_aval.shape)]), (
            pred_aval.shape, x_y_aval)
    bcast_pred = mhlo.BroadcastInDimOp(
        mlir.aval_to_ir_type(x_y_aval.update(dtype=np.dtype(np.bool_))),
        pred, mlir.dense_int_elements(list(range(len(pred_aval.shape))))).result
    return mhlo.SelectOp(bcast_pred, x, y).results
