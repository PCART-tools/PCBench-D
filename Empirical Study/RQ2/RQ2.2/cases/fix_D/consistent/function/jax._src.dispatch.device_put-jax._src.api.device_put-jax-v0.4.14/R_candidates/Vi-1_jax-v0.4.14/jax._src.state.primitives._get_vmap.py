def _get_vmap(batched_args, batched_dims, *, indexed_dims):
  axis_size, = {x.shape[d] for x, d in zip(batched_args, batched_dims)
                if d is not batching.not_mapped}
  ref, *idxs = batched_args
  ref_dim, *idx_dims = batched_dims

  ref_is_batched = ref_dim is not batching.not_mapped
  idx_is_batched = any(i_dim is not batching.not_mapped for i_dim in idx_dims)
  bdim_out = 0

  if idx_is_batched:
    # If at least one of the idx is batched, we broadcast them all and move the
    # batch dim to the front.
    idxs = tuple(batching.bdim_at_front(i, d, axis_size) for i, d
                 in zip(idxs, idx_dims))
  idxs_shape, = {i.shape for i in idxs} or [()]
  if ref_is_batched:
    # If ref is batched, we are doing a `get` with an additional axis. If `idxs`
    # are also batched, then we are indexing into the batch axis with an `iota`.
    indexed_dims = tuple_insert(indexed_dims, ref_dim, idx_is_batched)
    if idx_is_batched:
      # If we have batched idx, we need to insert the new iota index. The place
      # where we add in the new `iota` index is `ref_dim` so we need to compute
      # what `ref_dim` *would be* if we inserted it into `idxs` instead, because
      # `idxs` doesn't include the non indexed dims.
      idx_place = [i for i, i_dim in enumerate(indexed_dims)
                   if i_dim].index(ref_dim)
      iota = lax.broadcasted_iota(np.dtype('int32'), idxs_shape, 0)
      idxs = tuple_insert(idxs, idx_place, iota)
    else:
      bdim_out = _output_bdim(indexed_dims, ref_dim, idxs_shape)
  return get_p.bind(ref, *idxs, indexed_dims=indexed_dims), bdim_out
