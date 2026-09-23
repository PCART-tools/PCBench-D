def _pp_idx(ref_aval, idx: NDIndexer, context):
  docs = [
      _pp_dslice(d, s, context) if isinstance(s, Slice)
      else pp.text(jax_core.pp_var(s, context))
      for s, d in zip(idx.indices, ref_aval.shape)]
  if not docs:
    return pp.text("")
  doc = [docs[0]]
  for d in docs[1:]:
    doc.append(pp.text(","))
    doc.append(d)
  return pp.concat(doc)
