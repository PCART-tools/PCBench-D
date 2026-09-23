  def render(self):
    if self._rendered:
      raise ValueError("Can't call `render` twice.")
    self._root_elem.render()
    self._rendered = True
    self.append(self.elem)
