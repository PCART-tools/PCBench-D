def _swap_vmap(batched_args, batched_dims, *, indexed_dims):
  axis_size, = {x.shape[d] for x, d in zip(batched_args, batched_dims)
                if d is not batching.not_mapped}
  ref, val, *idxs = batched_args
  ref_dim, val_dim, *idx_dims = batched_dims
  ref_is_batched = ref_dim is not batching.not_mapped
  val_is_batched = val_dim is not batching.not_mapped
  idx_is_batched = any(i_dim is not batching.not_mapped for i_dim in idx_dims)
  if idx_is_batched:
    # If at least one of the idx is batched, we broadcast them all and move the
    # batch dim to the front.
    idxs = tuple(batching.bdim_at_front(i, d, axis_size) for i, d
                 in zip(idxs, idx_dims))
  idxs_shape, = {i.shape for i in idxs} or [()]
  if ref_is_batched and not idx_is_batched:
    indexed_dims = tuple_insert(indexed_dims, ref_dim, False)
    bdim_out = _output_bdim(indexed_dims, ref_dim, idxs_shape)
    if not val_is_batched:
      val = batching.broadcast(val, axis_size, 0)
      val_dim = 0
    val = batching.moveaxis(val, val_dim, bdim_out)
  elif idx_is_batched:
    assert ref_is_batched and val_is_batched
    indexed_dims = tuple_insert(indexed_dims, ref_dim, True)
    idx_place = [i for i, i_dim in enumerate(indexed_dims)
                 if i_dim].index(ref_dim)
    iota = lax.broadcasted_iota(np.dtype('int32'), idxs_shape, 0)
    idxs = tuple_insert(idxs, idx_place, iota)
    val = batching.moveaxis(val, val_dim, 0)
    bdim_out = 0
  return swap_p.bind(ref, val, *idxs, indexed_dims=indexed_dims), bdim_out
