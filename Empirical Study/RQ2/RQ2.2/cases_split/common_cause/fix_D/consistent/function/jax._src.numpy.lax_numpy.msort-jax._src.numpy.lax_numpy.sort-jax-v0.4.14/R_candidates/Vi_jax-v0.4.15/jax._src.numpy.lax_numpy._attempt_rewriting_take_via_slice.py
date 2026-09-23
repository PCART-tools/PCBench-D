def _attempt_rewriting_take_via_slice(arr: Array, idx: Any, mode: str | None) -> Array | None:
  # attempt to compute _rewriting_take via lax.slice(); return None if not possible.
  idx = idx if isinstance(idx, tuple) else (idx,)

  if not all(isinstance(i, int) for i in arr.shape):
    return None
  if len(idx) > arr.ndim:
    return None
  if any(i is None for i in idx):
    return None  # TODO(jakevdp): handle newaxis case

  simple_revs = {i for i, ind in enumerate(idx) if _is_simple_reverse_slice(ind)}
  int_indices = {i for i, (ind, size) in enumerate(zip(idx, arr.shape))
                 if _is_valid_integer_index_for_slice(ind, size, mode)}
  contiguous_slices = {i for i, ind in enumerate(idx) if _is_contiguous_slice(ind)}

  # For sharded inputs, indexing (like x[0]) and partial slices (like x[:2] as
  # opposed to x[:]) lead to incorrect sharding semantics when computed via
  # dynamic_slice, so we fall back to gather.
  # TODO(yashkatariya): fix dynamic_slice with sharding
  is_sharded = (isinstance(arr, ArrayImpl) and
                not dispatch.is_single_device_sharding(arr.sharding))
  has_partial_slices = any(idx[i].indices(arr.shape[i]) != (0, arr.shape[i], 1)
                           for i in contiguous_slices)
  if is_sharded and (int_indices or has_partial_slices):
    return None

  if len(simple_revs) + len(int_indices) + len(contiguous_slices) != len(idx):
    return None

  if simple_revs:
    arr = lax.rev(arr, tuple(simple_revs))
    idx = tuple(slice(None) if i in simple_revs else ind
                for i, ind in enumerate(idx))
    contiguous_slices |= simple_revs

  if not (int_indices or has_partial_slices):
    return arr

  idx += (arr.ndim - len(idx)) * (slice(None),)
  start_indices: Sequence[ArrayLike] = []
  slice_sizes: Sequence[int] = []

  for ind, size in safe_zip(idx, arr.shape):
    if isinstance(ind, slice):
      start, stop, step = ind.indices(size)
      assert step == 1  # checked above
      start_indices.append(start)
      slice_sizes.append(max(0, stop - start))
    else:
      assert np.issubdtype(_dtype(ind), np.integer)  # checked above
      assert np.shape(ind) == ()  # checked above
      start_indices.append(ind)
      slice_sizes.append(1)
  # We must be careful with dtypes because dynamic_slice requires all
  # start indices to have matching types.
  if len(start_indices) > 1:
    start_indices = util.promote_dtypes(*start_indices)
  arr = lax.dynamic_slice(arr, start_indices=start_indices, slice_sizes=slice_sizes)
  if int_indices:
    arr = lax.squeeze(arr, tuple(int_indices))
  return arr
