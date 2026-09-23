@dataclasses.dataclass
class StaticDOMElement(DOMElement):
  """An immutable DOM element."""
  _uuid: str = dataclasses.field(init=False)
  name: str
  children: List[Union[str, DOMElement]]
  attrs: Dict[str, str]

  def html(self):
    attr_str = ""
    if self.attrs:
      attr_str = " " + (" ".join(
          [f"{key}=\"{value}\"" for key, value in self.attrs.items()]))
    children = []
    children = "\n".join([str(c) for c in self.children])
    return f"<{self.name}{attr_str}>{children}</{self.name}>"

  def render(self):
    display.display(display.HTML(self.html()))

  def attr(self, key: str) -> str:
    return self.attrs[key]

  def __str__(self):
    return self.html()

  def __repr__(self):
    return self.html()

  def append(self, child: DOMElement) -> DOMElement:
    return dataclasses.replace(self, children=[*self.children, child])

  def replace(self, **kwargs) -> DOMElement:
    return dataclasses.replace(self, **kwargs)
