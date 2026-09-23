  @property
  def in_avals(self):
    """Tree of input avals."""
    return tree_util.tree_map(lambda x: x.aval, self.args_info)
