@dataclasses.dataclass(frozen=True)
class JumbleTy:
  binder: core.Var
  length: int | Tracer | core.Var
  elt_ty: core.DShapedArray
  def __repr__(self) -> str:
    return f'Var{id(self.binder)}:{self.length} => {self.elt_ty}'
  replace = dataclasses.replace
