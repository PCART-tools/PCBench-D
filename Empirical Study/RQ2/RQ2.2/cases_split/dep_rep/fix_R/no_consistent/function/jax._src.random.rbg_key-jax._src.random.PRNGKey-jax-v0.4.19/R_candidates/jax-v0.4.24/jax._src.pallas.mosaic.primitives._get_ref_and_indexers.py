def _get_ref_and_indexers(ref):
  if isinstance(ref, state.RefView):
    return ref.ref, ref.indexers
  return ref, ()
