class JaxprInputEffect(Effect):
  """A side-effect associated with the input of a jaxpr.

  Note that the `input_index` includes constvars.
  """

  def __init__(self, input_index: Any):
    self.input_index = input_index

  def replace(self, *, input_index: Any | None = None):
    if input_index is None:
      input_index = self.input_index
    return self.__class__(input_index)

  def __eq__(self, other):
    if not isinstance(other, JaxprInputEffect):
      return NotImplemented
    return self.input_index == other.input_index

  def __hash__(self):
    return hash((self.__class__, self.input_index))

  def __repr__(self):
    return f"{self.__class__.__name__}({self.input_index})"
