  def tree_flatten(self):
    return self.consts, (self.jaxpr, self.in_tree, self.out_tree)
