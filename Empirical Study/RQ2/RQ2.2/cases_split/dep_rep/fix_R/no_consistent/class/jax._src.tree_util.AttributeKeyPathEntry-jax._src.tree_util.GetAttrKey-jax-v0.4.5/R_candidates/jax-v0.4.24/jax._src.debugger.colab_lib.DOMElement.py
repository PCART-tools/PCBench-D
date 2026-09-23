class DOMElement(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def render(self):
    pass
