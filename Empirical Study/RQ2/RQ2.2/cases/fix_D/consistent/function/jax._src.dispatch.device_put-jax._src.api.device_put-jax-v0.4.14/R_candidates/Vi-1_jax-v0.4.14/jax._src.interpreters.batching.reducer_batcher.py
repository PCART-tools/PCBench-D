def reducer_batcher(prim, ident, batched_args, batch_dims, axes, **params):
  def out_axis(axes, axis):
    return int(list(np.delete(np.arange(operand.ndim), axes)).index(axis))
  operand, = batched_args
  bdim, = batch_dims
  if isinstance(bdim, int):
    axes = tuple(np.where(np.less(axes, bdim), axes, np.add(axes, 1)))
    bdim_out = out_axis(axes, bdim)
    if 'input_shape' in params:
      params = dict(params, input_shape=operand.shape)
    return prim.bind(operand, axes=axes, **params), bdim_out
  elif isinstance(bdim, RaggedAxis):
    assert ident is not None, "TODO Ragged batching a reduction requires an identity"
    axes = tuple(np.where(np.less(axes, bdim.stacked_axis), axes, np.add(axes, 1)))
    bdim_out = out_axis(axes, bdim.stacked_axis)
    # For each ragged_axis, we either mask the operand there or append
    # it to the set of axes that will be ragged in the result.
    axes_to_mask = []
    ragged_axes_out = []
    for ragged_axis, segment_lengths in bdim.ragged_axes:
      if ragged_axis in axes:
        axes_to_mask.append((ragged_axis, segment_lengths))
      else:
        ragged_axes_out.append((out_axis(axes, ragged_axis), segment_lengths))
    operand = mask_ragged_axes(
        operand, ident, RaggedAxis(bdim.stacked_axis, tuple(axes_to_mask)))
    result = prim.bind(operand, axes=axes, **params)
    return result, make_batch_axis(operand.ndim, bdim_out, ragged_axes_out)
  else:
    assert False
