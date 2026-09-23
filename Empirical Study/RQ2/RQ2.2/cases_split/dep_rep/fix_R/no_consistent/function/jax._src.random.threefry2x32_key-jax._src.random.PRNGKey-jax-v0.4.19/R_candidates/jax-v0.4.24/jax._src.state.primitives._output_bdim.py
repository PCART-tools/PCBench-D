def _output_bdim(indexed_dims: tuple[bool, ...], ref_dim: int,
                 idxs_shape: tuple[int, ...]):
  num_idxs_to_left = sum(indexed_dims[:ref_dim])
  return ref_dim - num_idxs_to_left + len(idxs_shape)
