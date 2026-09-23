def ref_addupdate(ref_or_view: AbstractRef, idx: Indexer | None, x: Array) -> None:
  """Mutates a ref with an additive update i.e. `ref[idx] += x`."""
  ref, indexers = get_ref_and_indexers(ref_or_view, idx, "ref_addupdate")
  flat_indexers, tree = tree_util.tree_flatten(indexers)
  return addupdate_p.bind(ref, x, *flat_indexers, tree=tree)
