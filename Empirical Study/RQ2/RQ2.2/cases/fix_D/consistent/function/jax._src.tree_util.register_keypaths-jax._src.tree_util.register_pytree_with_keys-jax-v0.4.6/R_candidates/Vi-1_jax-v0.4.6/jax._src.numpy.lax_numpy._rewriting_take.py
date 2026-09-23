def _rewriting_take(arr, idx, indices_are_sorted=False, unique_indices=False,
                    mode=None, fill_value=None):
  # Computes arr[idx].
  # All supported cases of indexing can be implemented as an XLA gather,
  # followed by an optional reverse and broadcast_in_dim.

  # Handle some special cases, falling back if error messages might differ.
  if (arr.ndim > 0 and isinstance(idx, (int, np.integer)) and
      not isinstance(idx, (bool, np.bool_)) and isinstance(arr.shape[0], int)):
    if 0 <= idx < arr.shape[0]:
      # Use dynamic rather than static index here to avoid slow repeated execution:
      # See https://github.com/google/jax/issues/12198
      return lax.dynamic_index_in_dim(arr, idx, keepdims=False)
  if (arr.ndim > 0 and isinstance(arr.shape[0], int) and
      isinstance(idx, slice) and
      (type(idx.start) is int or idx.start is None) and
      (type(idx.stop)  is int or idx.stop is  None) and
      (type(idx.step)  is int or idx.step is  None)):
    n = arr.shape[0]
    start = idx.start if idx.start is not None else 0
    stop  = idx.stop  if idx.stop  is not None else n
    step  = idx.step  if idx.step  is not None else 1
    if (0 <= start < n and 0 <= stop <= n and 0 < step and
        (start, stop, step) != (0, n, 1)):
      if _any(isinstance(d, core.Tracer) for d in arr.shape[1:]):
        if step == 1:  # TODO(mattjj, sharadmv): handle step != 1
          return lax.dynamic_slice_in_dim(arr, start, _max(0, stop - start), 0)
      elif step == 1:
        # Use dynamic rather than static slice here to avoid slow repeated execution:
        # See https://github.com/google/jax/issues/12198
        return lax.dynamic_slice_in_dim(arr, start, _max(0, stop - start), 0)
      else:
        return lax.slice_in_dim(arr, start, stop, step)

  # TODO(mattjj,dougalm): expand dynamic shape indexing support
  if jax.config.jax_dynamic_shapes and arr.ndim > 0:
    try: aval = core.get_aval(idx)
    except: pass
    else:
      if (isinstance(aval, core.DShapedArray) and aval.shape == () and
          dtypes.issubdtype(aval.dtype, np.integer) and
          not dtypes.issubdtype(aval.dtype, dtypes.bool_) and
          isinstance(arr.shape[0], int)):
        return lax.dynamic_index_in_dim(arr, idx, keepdims=False)

  treedef, static_idx, dynamic_idx = _split_index_for_jit(idx, arr.shape)
  return _gather(arr, treedef, static_idx, dynamic_idx, indices_are_sorted,
                 unique_indices, mode, fill_value)
