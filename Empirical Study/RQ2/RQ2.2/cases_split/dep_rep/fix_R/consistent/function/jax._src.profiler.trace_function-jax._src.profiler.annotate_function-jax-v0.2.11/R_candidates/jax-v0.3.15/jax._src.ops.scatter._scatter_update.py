def _scatter_update(x, idx, y, scatter_op, indices_are_sorted,
                    unique_indices, mode=None, normalize_indices=True):
  """Helper for indexed updates.

  Computes the value of x that would result from computing::
    x[idx] op= y
  except in a pure functional way, with no in-place updating.

  Args:
    x: ndarray to be updated.
    idx: None, an integer, a slice, an ellipsis, an ndarray with integer dtype,
      or a tuple of those indicating the locations of `x` into which to scatter-
      update the values in `y`.
    y: values to be scattered.
    scatter_op: callable, one of lax.scatter, lax.scatter_add, lax.scatter_min,
      or lax_scatter_max.
    indices_are_sorted: whether `idx` is known to be sorted
    unique_indices: whether `idx` is known to be free of duplicates

  Returns:
    An ndarray representing an updated `x` after performing the scatter-update.
  """

  x = jnp.asarray(x)
  y = jnp.asarray(y)
  # XLA gathers and scatters are very similar in structure; the scatter logic
  # is more or less a transpose of the gather equivalent.
  treedef, static_idx, dynamic_idx = jnp._split_index_for_jit(idx, x.shape)
  return _scatter_impl(x, y, scatter_op, treedef, static_idx, dynamic_idx,
                       indices_are_sorted, unique_indices, mode,
                       normalize_indices)
