def ref_swap(ref_or_view: AbstractRef | RefView, idx: Indexer | None, value: Array,
             _function_name: str = "ref_swap") -> Array:
  """Sets a `Ref`'s value and returns the original value."""
  ref, indexers = get_ref_and_indexers(ref_or_view, idx, _function_name)
  flat_indexers, tree = tree_util.tree_flatten(indexers)
  return swap_p.bind(ref, value, *flat_indexers, tree=tree)
