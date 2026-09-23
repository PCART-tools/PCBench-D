def get_ref_and_indexers(
    ref_or_view: Any, idx: Indexer | None, function_name: str
) -> tuple[Any, tuple[indexing.NDIndexer, ...]]:
  if isinstance(ref_or_view, RefView):
    ref, indexers = ref_or_view.ref, ref_or_view.indexers
  else:
    ref, indexers = ref_or_view, ()
  ref_aval = core.get_aval(ref)
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"Can only call `{function_name}` on a `Ref`: {ref}.")
  if not isinstance(ref_aval.inner_aval, core.ShapedArray):
    return ref, ()
  if idx is None:
    return ref, indexers
  nd_indexer = indexing.NDIndexer.from_indices_shape(idx, ref_or_view.shape)
  return ref, (*indexers, nd_indexer)
