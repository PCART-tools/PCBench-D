def _unpack_idx(idx: Indexer, ndim: int
               ) -> tuple[tuple[Array, ...], tuple[bool, ...]]:
  if _is_trivial_indexer(idx):
    idx = tuple(slice(None) for _ in range(ndim))
  indexed_dims_ = []
  non_slice_idx = []
  for i in idx:
    if isinstance(i, slice):
      if i.start is not None or i.stop is not None or i.step is not None:
        raise NotImplementedError("Reference indexing only supports trivial slices")
      indexed_dims_.append(False)
    else:
      non_slice_idx.append(i)
      indexed_dims_.append(True)
  indexed_dims = indexed_dims_ + [False] * (ndim - len(indexed_dims_))
  import jax.numpy as jnp
  return (tuple(map(jnp.int32, non_slice_idx)), tuple(indexed_dims))
