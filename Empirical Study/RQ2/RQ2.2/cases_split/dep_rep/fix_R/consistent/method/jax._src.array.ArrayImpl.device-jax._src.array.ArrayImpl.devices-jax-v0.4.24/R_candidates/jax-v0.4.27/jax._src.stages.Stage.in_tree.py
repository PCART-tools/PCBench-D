  @property
  def in_tree(self) -> tree_util.PyTreeDef:
    """Tree structure of the pair (positional arguments, keyword arguments)."""
    return tree_util.tree_structure(self.args_info)
