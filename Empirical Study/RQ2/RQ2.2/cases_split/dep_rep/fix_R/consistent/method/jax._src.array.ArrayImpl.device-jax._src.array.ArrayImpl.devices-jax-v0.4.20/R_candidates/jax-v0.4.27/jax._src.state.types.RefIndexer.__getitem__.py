  def __getitem__(self, slc):
    if not isinstance(slc, tuple):
      slc = (slc,)
    indexer = indexing.NDIndexer.from_indices_shape(slc, self.ref_or_view.shape)
    if isinstance(self.ref_or_view, RefView):
      view = self.ref_or_view
      return RefView(view.ref, (*view.indexers, indexer))
    return RefView(self.ref_or_view, (indexer,))
