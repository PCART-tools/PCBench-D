  def write(self, v: core.Var, val: Any) -> None:
    self.env[v] = val
