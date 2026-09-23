def reducer_batcher(prim, batched_args, batch_dims, axes, **params):
  operand, = batched_args
  bdim, = batch_dims
  if isinstance(bdim, int):
    axes = tuple(np.where(np.less(axes, bdim), axes, np.add(axes, 1)))
    bdim_out = int(list(np.delete(np.arange(operand.ndim), axes)).index(bdim))
    if 'input_shape' in params:
      params = dict(params, input_shape=operand.shape)
    return prim.bind(operand, axes=axes, **params), bdim_out
  elif isinstance(bdim, ConcatAxis):
    if bdim.axis in axes:
      other_axes = [i for i in axes if i != bdim.axis]
      if other_axes:
        operand = prim.bind(operand, axes=other_axes, **params)
      c_axis = bdim.axis - sum(d < bdim.axis for d in other_axes)
      operand = bdim_at_front(operand, c_axis, operand.shape[c_axis])
      return segment_sum(operand, bdim.segment_lengths), 0
    else:
      raise NotImplementedError  # TODO(mattjj)
  else:
    assert False
