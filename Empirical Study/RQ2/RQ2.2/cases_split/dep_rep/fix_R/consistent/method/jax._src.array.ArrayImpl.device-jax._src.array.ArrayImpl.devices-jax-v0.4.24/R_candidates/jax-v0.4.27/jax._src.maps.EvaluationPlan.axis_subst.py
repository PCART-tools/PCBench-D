  @property
  def axis_subst(self) -> core.AxisSubst:
    return lambda name: self.axis_subst_dict.get(name, (name,))
