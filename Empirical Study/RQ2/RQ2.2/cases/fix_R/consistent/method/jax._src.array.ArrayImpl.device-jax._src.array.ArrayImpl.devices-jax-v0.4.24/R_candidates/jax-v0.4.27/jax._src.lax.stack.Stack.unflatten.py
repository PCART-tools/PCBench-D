  @staticmethod
  def unflatten(treedef, leaves):
    return Stack(leaves[0], jax.tree_util.tree_unflatten(treedef, leaves[1:]))
