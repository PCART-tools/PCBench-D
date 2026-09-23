  def output_layouts(self):
    layouts_flat = self._executable.output_layouts()
    assert all(isinstance(l, Layout) for l in layouts_flat)
    return tree_util.tree_unflatten(self.out_tree, layouts_flat)  # pytype: disable=attribute-error
