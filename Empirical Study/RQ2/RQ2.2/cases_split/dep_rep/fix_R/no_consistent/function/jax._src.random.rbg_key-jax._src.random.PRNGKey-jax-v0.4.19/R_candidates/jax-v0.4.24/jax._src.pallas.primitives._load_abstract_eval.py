def _load_abstract_eval(*avals_flat, args_tree, **_):
  ref, indexers, _, _ = args_tree.unflatten(avals_flat)
  return (
      jax_core.ShapedArray(indexers[-1].get_indexer_shape(), ref.dtype),
      {state.ReadEffect(0)},
  )
