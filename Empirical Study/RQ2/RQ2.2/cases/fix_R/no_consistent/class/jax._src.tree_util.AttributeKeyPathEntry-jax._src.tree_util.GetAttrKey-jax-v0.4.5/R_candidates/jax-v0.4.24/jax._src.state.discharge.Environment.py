@dataclasses.dataclass
class Environment:
  env: dict[core.Var, Any]

  def read(self, v: core.Atom) -> Any:
    if type(v) is core.Literal:
      return v.val
    assert isinstance(v, core.Var)
    return self.env[v]

  def write(self, v: core.Var, val: Any) -> None:
    self.env[v] = val
