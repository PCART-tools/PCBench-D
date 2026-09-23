  def flatten(self):
    leaves, treedef = jax.tree_util.tree_flatten(self._data)
    return ([self._size] + leaves), treedef
