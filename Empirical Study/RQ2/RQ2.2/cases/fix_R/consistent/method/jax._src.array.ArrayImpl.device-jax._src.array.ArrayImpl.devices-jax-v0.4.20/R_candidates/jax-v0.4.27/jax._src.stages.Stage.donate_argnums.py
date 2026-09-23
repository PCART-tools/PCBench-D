  @property
  def donate_argnums(self):
    """Flat tuple of donated argument indices."""
    return tuple(
        i for i, x in enumerate(tree_util.tree_leaves(self.args_info))
        if x.donated)
