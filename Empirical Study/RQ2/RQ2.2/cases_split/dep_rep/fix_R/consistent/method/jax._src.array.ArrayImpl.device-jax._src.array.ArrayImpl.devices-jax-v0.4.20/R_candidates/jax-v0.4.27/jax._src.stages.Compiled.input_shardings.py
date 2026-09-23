  @property
  def input_shardings(self):  # PyTree[sharding.XLACompatibleSharding]
    shardings_flat = self._executable.input_shardings()
    return tree_util.tree_unflatten(self.in_tree, shardings_flat)  # pytype: disable=attribute-error
