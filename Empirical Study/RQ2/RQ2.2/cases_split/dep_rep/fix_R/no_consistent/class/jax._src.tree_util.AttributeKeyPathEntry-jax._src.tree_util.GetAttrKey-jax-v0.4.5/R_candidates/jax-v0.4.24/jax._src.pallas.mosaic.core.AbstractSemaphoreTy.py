class AbstractSemaphoreTy(dtypes.ExtendedDType):
  name: str

  def __repr__(self) -> str:
    return self.name

  def __eq__(self, other):
    return self.__class__ == other.__class__

  def __hash__(self) -> int:
    return hash((self.__class__))
