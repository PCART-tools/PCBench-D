def _pred_bcast_select_hlo(ctx,
    pred_aval: core.ShapedArray, pred: ir.Value, xs: Sequence[ir.Value],
    ys: Sequence[ir.Value], x_y_aval: core.AbstractValue) -> Sequence[ir.Value]:
  if x_y_aval is core.abstract_token:
    x, = xs
    y, = ys
    return [hlo.AfterAllOp([x, y]).result]
  else:
    assert isinstance(x_y_aval, core.ShapedArray), x_y_aval
    x, = xs
    y, = ys
    assert x.type == y.type, (x.type, y.type)
    assert (pred_aval.shape == x_y_aval.shape[:len(pred_aval.shape)]), (
            pred_aval.shape, x_y_aval)
    x_y_aval = core.physical_aval(x_y_aval)
    bcast_pred = mlir.broadcast_in_dim(
        ctx, pred, core.DShapedArray(x_y_aval.shape, np.dtype(np.bool_)),
        broadcast_dimensions=list(range(len(pred_aval.shape))))
    return hlo.SelectOp(bcast_pred, x, y).results
