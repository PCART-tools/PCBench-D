  @classmethod
  def tree_unflatten(cls, data, flat_idx):
    idx_tree, shape, int_indexer_shape = data
    indices = tree_util.tree_unflatten(idx_tree, flat_idx)
    return NDIndexer(tuple(indices), shape, int_indexer_shape)
