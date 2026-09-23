  def __iter__(self):
    return iter((self.jaxpr, self.in_tree, self.out_tree, self.consts))
