def _segment_update(name: str,
                    data: Array,
                    segment_ids: Array,
                    scatter_op: Callable,
                    num_segments: Optional[int] = None,
                    indices_are_sorted: bool = False,
                    unique_indices: bool = False,
                    bucket_size: Optional[int] = None,
                    reducer: Optional[Callable] = None,
                    mode: Optional[lax.GatherScatterMode] = None) -> Array:
  jnp._check_arraylike(name, data, segment_ids)
  mode = lax.GatherScatterMode.FILL_OR_DROP if mode is None else mode
  data = jnp.asarray(data)
  segment_ids = jnp.asarray(segment_ids)
  dtype = data.dtype
  if num_segments is None:
    num_segments = jnp.max(segment_ids) + 1
  num_segments = core.concrete_or_error(int, num_segments, "segment_sum() `num_segments` argument.")
  if num_segments is not None and num_segments < 0:
    raise ValueError("num_segments must be non-negative.")


  num_buckets = 1 if bucket_size is None \
                  else util.ceil_of_ratio(segment_ids.size, bucket_size)
  if num_buckets == 1:
    out = jnp.full((num_segments,) + data.shape[1:],
                   _get_identity(scatter_op, dtype), dtype=dtype)
    return _scatter_update(
      out, segment_ids, data, scatter_op, indices_are_sorted,
      unique_indices, normalize_indices=False, mode=mode)

  # Bucketize indices and perform segment_update on each bucket to improve
  # numerical stability for operations like product and sum.
  assert reducer is not None
  out = jnp.full((num_buckets, num_segments) + data.shape[1:],
                 _get_identity(scatter_op, dtype), dtype=dtype)
  out = _scatter_update(
    out, np.index_exp[lax.div(jnp.arange(segment_ids.shape[0]), bucket_size),
                      segment_ids[None, :]],
    data, scatter_op, indices_are_sorted,
    unique_indices, normalize_indices=False, mode=mode)
  return reducer(out, axis=0).astype(dtype)
