  @property
  def frame(self):
    return self.main.jaxpr_stack[-1]  # pytype: disable=attribute-error
