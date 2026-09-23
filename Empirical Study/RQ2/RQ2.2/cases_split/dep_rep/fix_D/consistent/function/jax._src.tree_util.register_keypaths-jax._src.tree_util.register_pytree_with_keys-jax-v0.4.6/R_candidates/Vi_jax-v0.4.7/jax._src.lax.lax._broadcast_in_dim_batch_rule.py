def _broadcast_in_dim_batch_rule(batched_args, batch_dims, shape,
                                 broadcast_dimensions):
  operand, *dyn_shape = batched_args
  operand_bdim, *dyn_shape_bdims = batch_dims
  if len(dyn_shape) > 1: raise NotImplementedError
  if (operand_bdim is not None and
      (not dyn_shape_bdims or dyn_shape_bdims[0] is None)):
    new_operand = batching.moveaxis(operand, operand_bdim, 0)
    new_shape = (operand.shape[operand_bdim],) + _merge_dyn_shape(shape, dyn_shape)
    new_broadcast_dimensions = (0,) + tuple(np.add(1, broadcast_dimensions))
    return broadcast_in_dim(new_operand, new_shape, new_broadcast_dimensions), 0
  elif (operand_bdim is None and dyn_shape_bdims and
        dyn_shape_bdims[0] is not None):
    (d,), (d_bdim,) = dyn_shape, dyn_shape_bdims  # NotImplementedError above
    assert d_bdim == 0  # must be scalar in the program to be batched
    new_shape = _merge_dyn_shape(shape, (int(d.sum()),))
    out = broadcast_in_dim(operand, new_shape, broadcast_dimensions)
    idx, = (i for i, s in enumerate(shape) if s is None)
    return out, batching.ConcatAxis(idx, d)
  else:
    raise NotImplementedError  # TODO(mattjj)
