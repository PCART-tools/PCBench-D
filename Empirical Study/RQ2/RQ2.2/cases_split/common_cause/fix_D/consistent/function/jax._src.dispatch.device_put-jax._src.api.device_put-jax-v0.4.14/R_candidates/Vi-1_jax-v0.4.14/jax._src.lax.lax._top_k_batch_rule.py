def _top_k_batch_rule(batched_args, batch_dims, *, k):
  operand, = batched_args
  bdim, = batch_dims
  if bdim == operand.ndim-1:
    perm = np.arange(operand.ndim)
    perm[bdim-1], perm[bdim] = perm[bdim], perm[bdim-1]
    top_k_v, top_k_i = top_k(transpose(operand, perm), k=k)
    return (transpose(top_k_v, perm),
            transpose(top_k_i, perm)), (bdim, bdim)
  else:
    return top_k(operand, k=k), (bdim, bdim)
