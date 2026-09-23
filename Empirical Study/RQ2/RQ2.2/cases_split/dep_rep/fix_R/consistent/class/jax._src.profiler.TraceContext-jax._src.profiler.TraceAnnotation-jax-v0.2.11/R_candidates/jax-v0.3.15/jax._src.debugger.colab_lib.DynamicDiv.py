@dataclasses.dataclass
class DynamicDiv(DynamicDOMElement):
  """A `div` that can be edited."""
  _uuid: str = dataclasses.field(init=False)
  _root_elem: DOMElement = dataclasses.field(init=False)
  elem: Union[DOMElement, str]

  def __post_init__(self):
    self._uuid = str(uuid.uuid4())
    self._rendered = False
    self._root_elem = div(id=self.tag)

  @property
  def tag(self):
    return f"tag-{self._uuid}"

  def render(self):
    if self._rendered:
      raise ValueError("Can't call `render` twice.")
    self._root_elem.render()
    self._rendered = True
    self.append(self.elem)

  def append(self, child: DOMElement):
    if not self._rendered:
      self.render()
    with output.use_tags([self.tag]):
      with output.redirect_to_element(f"#{self.tag}"):
        child.render()

  def update(self, elem: DOMElement):
    self.clear()
    self.elem = elem
    self.render()

  def clear(self):
    output.clear(output_tags=[self.tag])
    self._rendered = False
