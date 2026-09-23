def _pp_indexers(
    context: core.JaxprPpContext, indexers: tuple[indexing.NDIndexer, ...],
):
  if not indexers:
    return pp.text("[...]")
  return pp.concat(
      [pp_indexer(context, indexer) for indexer in indexers]
  )
