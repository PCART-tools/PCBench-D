def _transpose_batch_rule(batched_args, batch_dims, *, permutation):
  operand, = batched_args
  bdim, = batch_dims
  stack_dim = bdim.stacked_axis if isinstance(bdim, RaggedAxis) else bdim
  perm = (stack_dim,) + tuple(i if i < stack_dim else i+1 for i in permutation)
  if isinstance(bdim, RaggedAxis):
    res_bdim = batching.transpose_ragged_axes(bdim.move_stacked_axis(0), perm)
  else:
    res_bdim = 0
  return transpose(operand, perm), res_bdim
