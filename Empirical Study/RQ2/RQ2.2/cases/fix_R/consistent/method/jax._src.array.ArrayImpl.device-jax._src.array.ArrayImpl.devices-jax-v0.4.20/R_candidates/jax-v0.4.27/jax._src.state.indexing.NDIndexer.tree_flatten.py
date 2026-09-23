  def tree_flatten(self):
    flat_idx, idx_tree = tree_util.tree_flatten(self.indices)
    return flat_idx, (idx_tree, self.shape, self.int_indexer_shape)
