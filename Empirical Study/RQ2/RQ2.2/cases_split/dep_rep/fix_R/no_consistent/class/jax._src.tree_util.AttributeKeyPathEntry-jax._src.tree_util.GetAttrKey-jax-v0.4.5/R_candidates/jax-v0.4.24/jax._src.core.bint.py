@dataclass(frozen=True)
class bint(dtypes.ExtendedDType):
  bound: int

  @property
  def type(self) -> type:
    return dtypes.extended

  @property
  def name(self) -> str:
    return f'bint{{≤{self.bound}}}'

  def __str__(self) -> str:
    return self.name
