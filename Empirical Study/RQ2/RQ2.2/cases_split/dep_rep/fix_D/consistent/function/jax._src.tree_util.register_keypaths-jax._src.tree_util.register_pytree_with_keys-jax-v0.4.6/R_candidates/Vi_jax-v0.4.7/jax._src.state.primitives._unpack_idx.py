def _unpack_idx(idx: Indexer, ndim: int
               ) -> Tuple[Tuple[Array, ...], Tuple[bool, ...]]:
  if _is_trivial_indexer(idx):
    idx = tuple(slice(None) for _ in range(ndim))
  indexed_dims_ = [type(i) != slice for i in idx]
  _, non_slice_idx = partition_list(indexed_dims_, idx)
  indexed_dims = indexed_dims_ + [False] * (ndim - len(indexed_dims_))
  import jax.numpy as jnp
  return (tuple(map(jnp.int32, non_slice_idx)), tuple(indexed_dims))
