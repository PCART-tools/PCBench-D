  def append(self, child: DOMElement) -> DOMElement:
    return dataclasses.replace(self, children=[*self.children, child])
