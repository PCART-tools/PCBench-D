def pp_indexer(context: core.JaxprPpContext,indexer: indexing.NDIndexer
                ) -> pp.Doc:
  indices = []
  for idx, dim in zip(indexer.indices, indexer.shape):
    if isinstance(idx, indexing.Slice):
      indices.append(_pp_slice(context, dim, idx))
    else:
      indices.append(core.pp_var(idx, context))  # type: ignore
  return pp.concat([pp.text("["), pp.text(','.join(indices)), pp.text("]")])
