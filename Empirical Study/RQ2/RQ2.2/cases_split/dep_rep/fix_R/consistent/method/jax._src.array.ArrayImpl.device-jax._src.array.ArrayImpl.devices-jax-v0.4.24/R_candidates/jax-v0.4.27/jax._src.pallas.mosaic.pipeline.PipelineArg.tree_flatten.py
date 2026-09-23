  def tree_flatten(self):
    return ((self.input, self.out, self.in_out), None)
