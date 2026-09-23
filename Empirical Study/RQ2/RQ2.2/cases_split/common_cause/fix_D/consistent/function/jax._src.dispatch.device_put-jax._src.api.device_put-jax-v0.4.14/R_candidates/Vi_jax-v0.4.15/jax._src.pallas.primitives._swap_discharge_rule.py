def _swap_discharge_rule(in_avals, out_avals, ref, val, *args, args_tree,
                         masked, eviction_policy):
  idx, *_ = tree_util.tree_unflatten(args_tree, args)
  if all(isinstance(s, Slice) or s.shape == () for s in idx.indices):
    indices = idx.indices
    scalar_dims = [not isinstance(s, Slice) and s.shape == () for s in indices]
    slice_starts = [s.start if isinstance(s, Slice) else s for s in indices]
    slice_sizes = tuple(s.size if isinstance(s, Slice) else 1 for s in indices)
    val_indexer = tuple(None if scalar else slice(None) for scalar in scalar_dims)
    val = val[val_indexer]
    x_new = lax.dynamic_update_slice(ref, val, start_indices=slice_starts)
    out_ones = lax.dynamic_slice(ref, slice_starts, slice_sizes=slice_sizes)
    out_indexer = tuple(0 if scalar else slice(None) for scalar in scalar_dims)
    out = out_ones[out_indexer]
  elif all(not isinstance(s, Slice) for s in idx.indices):
    out = ref[idx.indices]
    x_new = ref.at[idx.indices].set(val)
  else:
    raise NotImplementedError
  return (x_new,) + (None,) * (len(in_avals) - 1), out
