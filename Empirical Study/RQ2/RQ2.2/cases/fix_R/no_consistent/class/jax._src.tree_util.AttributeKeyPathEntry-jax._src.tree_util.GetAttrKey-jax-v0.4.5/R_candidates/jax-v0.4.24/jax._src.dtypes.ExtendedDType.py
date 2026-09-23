class ExtendedDType(StrictABC):
  """Abstract Base Class for extended dtypes"""
  @property
  @abc.abstractmethod
  def type(self) -> type: ...
