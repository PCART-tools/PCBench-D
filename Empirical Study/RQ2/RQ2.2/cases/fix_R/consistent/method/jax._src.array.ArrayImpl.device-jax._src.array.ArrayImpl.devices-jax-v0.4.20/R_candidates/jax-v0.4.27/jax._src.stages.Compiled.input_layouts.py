  def input_layouts(self):
    layouts_flat = self._executable.input_layouts()
    assert all(isinstance(l, Layout) for l in layouts_flat)
    # Some input layouts got DCE'd
    if self.in_tree.num_leaves > len(layouts_flat):
      iter_layouts_flat = iter(layouts_flat)
      layouts_flat = [next(iter_layouts_flat) if i in self._executable._kept_var_idx
                      else Layout() for i in range(self.in_tree.num_leaves)]
    return tree_util.tree_unflatten(self.in_tree, layouts_flat)  # pytype: disable=attribute-error
