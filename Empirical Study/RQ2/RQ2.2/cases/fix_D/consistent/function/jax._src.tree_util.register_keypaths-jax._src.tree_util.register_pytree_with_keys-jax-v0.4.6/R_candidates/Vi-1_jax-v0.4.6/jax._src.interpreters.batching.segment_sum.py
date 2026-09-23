def segment_sum(operand, segment_lens):
  scat_idx = jax.numpy.cumsum(segment_lens) - segment_lens
  segment_ids = jax.numpy.cumsum(
      jax.numpy.zeros(operand.shape[0], 'int32').at[scat_idx].set(1)) - 1
  out = jax.numpy.zeros((len(segment_lens), *operand.shape[1:]),
                        operand.dtype).at[segment_ids].add(operand)
  return out
