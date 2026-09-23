def ref_get(ref_or_view: Any, idx: Indexer | None = None) -> Array:
  """Reads a value from a `Ref`, a.k.a. value <- ref[idx]."""
  ref, indexers = get_ref_and_indexers(ref_or_view, idx, "ref_get")
  flat_indexers, tree = tree_util.tree_flatten(indexers)
  return get_p.bind(ref, *flat_indexers, tree=tree)
