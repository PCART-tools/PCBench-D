def _swap_discharge_rule(in_avals, out_avals, *args_flat, args_tree, **_):
  del out_avals  # Unused.
  ref, indexers, val, mask = args_tree.unflatten(args_flat)
  if len(indexers) > 1:
    raise NotImplementedError("Only one indexer supported in discharge rule.")
  idx = indexers[0]
  if all((isinstance(s, Slice) or not s.shape) for s in idx.indices):
    indices = idx.indices
    scalar_dims = [
        i
        for i, s in enumerate(indices)
        if not isinstance(s, Slice) and not s.shape
    ]
    slice_starts = [s.start if isinstance(s, Slice) else s for s in indices]
    slice_sizes = tuple(s.size if isinstance(s, Slice) else 1 for s in indices)
    out = lax.dynamic_slice(ref, slice_starts, slice_sizes=slice_sizes)
    out = jnp.squeeze(out, scalar_dims)
    if mask is not None:
      out_ = out
      out = jnp.where(mask, out, val)
      val = jnp.where(mask, val, out_)
    val = jnp.expand_dims(val, scalar_dims)
    x_new = lax.dynamic_update_slice(ref, val, start_indices=slice_starts)
  elif all(not isinstance(s, Slice) for s in idx.indices):
    out = ref[idx.indices]
    if mask is not None:
      out_ = out
      out = jnp.where(mask, out, val)
      val = jnp.where(mask, val, out_)
    x_new = ref.at[idx.indices].set(val)
  else:
    raise NotImplementedError
  return (x_new,) + (None,) * (len(in_avals) - 1), out
