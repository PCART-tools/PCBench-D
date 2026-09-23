def _scatter_impl(x, y, scatter_op, treedef, static_idx, dynamic_idx,
                  indices_are_sorted, unique_indices, mode,
                  normalize_indices):
  dtype = lax.dtype(x)
  weak_type = dtypes.is_weakly_typed(x)

  if not dtypes.safe_to_cast(y, x):
    # TODO(jakevdp): change this to an error after the deprecation period.
    warnings.warn(
      "scatter inputs have incompatible types: cannot safely cast value "
      f"from dtype={lax.dtype(y)} to dtype={lax.dtype(x)} with "
      f"jax_numpy_dtype_promotion={config.numpy_dtype_promotion.value!r}. "
      "In future JAX releases this will result in an error.",
      FutureWarning)

  idx = jnp._merge_static_and_dynamic_indices(treedef, static_idx, dynamic_idx)
  indexer = jnp._index_to_gather(jnp.shape(x), idx,
                                 normalize_indices=normalize_indices)

  # Avoid calling scatter if the slice shape is empty, both as a fast path and
  # to handle cases like zeros(0)[array([], int32)].
  if core.is_empty_shape(indexer.slice_shape):
    return x

  x, y = promote_dtypes(x, y)

  # Broadcast `y` to the slice output shape.
  y = jnp.broadcast_to(y, tuple(indexer.slice_shape))
  # Collapse any `None`/`jnp.newaxis` dimensions.
  y = jnp.squeeze(y, axis=indexer.newaxis_dims)
  if indexer.reversed_y_dims:
    y = lax.rev(y, indexer.reversed_y_dims)

  # Transpose the gather dimensions into scatter dimensions (cf.
  # lax._gather_transpose_rule)
  dnums = lax.ScatterDimensionNumbers(
    update_window_dims=indexer.dnums.offset_dims,
    inserted_window_dims=indexer.dnums.collapsed_slice_dims,
    scatter_dims_to_operand_dims=indexer.dnums.start_index_map
  )
  out = scatter_op(
    x, indexer.gather_indices, y, dnums,
    indices_are_sorted=indexer.indices_are_sorted or indices_are_sorted,
    unique_indices=indexer.unique_indices or unique_indices,
    mode=mode)
  return lax_internal._convert_element_type(out, dtype, weak_type)
