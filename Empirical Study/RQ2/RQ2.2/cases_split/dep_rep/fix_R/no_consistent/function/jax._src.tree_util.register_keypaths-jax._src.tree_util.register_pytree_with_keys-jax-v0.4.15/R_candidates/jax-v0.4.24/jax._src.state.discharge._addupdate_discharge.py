def _addupdate_discharge(x, val, idx, tree):
  indexers = tree_util.tree_unflatten(tree, idx)
  if len(indexers) > 1:
    raise NotImplementedError("Only single indexer is supported.")
  indexer = indexers[0]
  if _is_trivial_indexer(indexer):
    return x + val
  # If everything in the indexer is a slice or ()-shaped, we can also
  # use `lax.dynamic_slice` with 1-sized slices for ()-shaped indices.
  # We need to squeeze out the the 1-sized slices at the end.
  if maybe_slice := _maybe_convert_to_dynamic_slice(indexer):
    starts, sizes, squeeze_dims = maybe_slice
    x_old = lax_slicing.dynamic_slice(x, starts, sizes)
    val = lax.expand_dims(val, squeeze_dims)
    y = lax_slicing.dynamic_update_slice(x, x_old + val, starts)
    return y
  indexer = _convert_to_array_indexer(indexer)
  return _prepend_scatter(x, indexer, val, add=True)
