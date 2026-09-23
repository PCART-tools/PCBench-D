def _load_discharge_rule(in_avals, out_avals, *args_flat, args_tree, **_):
  del out_avals  # Unused.
  ref, indexers, mask, other = args_tree.unflatten(args_flat)
  # TODO(sharadmv): add support for multiple indexers
  if len(indexers) > 1:
    raise NotImplementedError("Only one indexer supported in discharge rule.")
  idx = indexers[0]
  if all((isinstance(s, Slice) or not s.shape) for s in idx.indices):
    indices = idx.indices
    scalar_dims = [not isinstance(s, Slice) and not s.shape for s in indices]
    slice_starts = [s.start if isinstance(s, Slice) else s for s in indices]
    slice_sizes = tuple(s.size if isinstance(s, Slice) else 1 for s in indices)
    out_ones = lax.dynamic_slice(ref, slice_starts, slice_sizes=slice_sizes)
    out_indexer = tuple(0 if scalar else slice(None) for scalar in scalar_dims)
    out = out_ones[out_indexer]
  elif all(not isinstance(s, Slice) for s in idx.indices):
    out = ref[idx.indices]
  else:
    raise NotImplementedError
  if mask is not None and other is not None:
    out = jnp.where(mask, out, other)
  return (None,) * len(in_avals), out
