def _rewriting_take(arr, idx, indices_are_sorted=False, unique_indices=False,
                    mode=None, fill_value=None):
  # Computes arr[idx].
  # All supported cases of indexing can be implemented as an XLA gather,
  # followed by an optional reverse and broadcast_in_dim.
  arr = asarray(arr)

  # TODO(mattjj,dougalm): expand dynamic shape indexing support
  if (jax.config.jax_dynamic_shapes and type(idx) is slice and idx.step is None
      and (isinstance(idx.start, core.Tracer) or isinstance(idx.stop, core.Tracer))
      and arr.shape):
    start = 0 if idx.start is None else idx.start
    stop = arr.shape[0] if idx.stop is None else idx.stop
    return _getslice(arr, start, stop)

  treedef, static_idx, dynamic_idx = _split_index_for_jit(idx, arr.shape)
  return _gather(arr, treedef, static_idx, dynamic_idx, indices_are_sorted,
                 unique_indices, mode, fill_value)
