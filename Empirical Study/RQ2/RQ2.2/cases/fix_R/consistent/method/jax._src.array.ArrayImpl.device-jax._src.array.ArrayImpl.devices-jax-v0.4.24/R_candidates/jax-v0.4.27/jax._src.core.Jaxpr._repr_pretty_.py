  def _repr_pretty_(self, p, cycle):
    return p.text(self.pretty_print(use_color=True))
