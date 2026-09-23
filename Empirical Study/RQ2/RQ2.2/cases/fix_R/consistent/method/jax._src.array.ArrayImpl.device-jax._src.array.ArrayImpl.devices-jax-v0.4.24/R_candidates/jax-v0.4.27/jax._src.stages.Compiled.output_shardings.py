  @property
  def output_shardings(self):  # PyTree[sharding.XLACompatibleSharding]
    shardings_flat = self._executable.output_shardings()
    return tree_util.tree_unflatten(self.out_tree, shardings_flat)  # pytype: disable=attribute-error
