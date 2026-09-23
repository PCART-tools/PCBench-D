def _transpose_batch_rule(batched_args, batch_dims, *, permutation):
  operand, = batched_args
  bdim, = batch_dims
  perm = (bdim,) + tuple(i if i < bdim else i+1 for i in permutation)
  return transpose(operand, perm), 0
