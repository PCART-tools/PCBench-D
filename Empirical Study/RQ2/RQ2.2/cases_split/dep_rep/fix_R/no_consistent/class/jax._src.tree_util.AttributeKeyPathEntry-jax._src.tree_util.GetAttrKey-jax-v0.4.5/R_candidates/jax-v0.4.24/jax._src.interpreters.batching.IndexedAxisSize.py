@dataclasses.dataclass(frozen=True)
class IndexedAxisSize:
  idx: core.Var
  lengths: Array | core.Var | Tracer
  def __repr__(self) -> str:
    return f'{self.lengths}.Var{id(self.idx)}'
  replace = dataclasses.replace
