class DynamicDOMElement(DOMElement):
  """A DOM element that can be mutated."""

  @abc.abstractmethod
  def render(self):
    pass

  @abc.abstractmethod
  def append(self, child: DOMElement):
    pass

  @abc.abstractmethod
  def update(self, elem: DOMElement):
    pass

  @abc.abstractmethod
  def clear(self):
    pass
