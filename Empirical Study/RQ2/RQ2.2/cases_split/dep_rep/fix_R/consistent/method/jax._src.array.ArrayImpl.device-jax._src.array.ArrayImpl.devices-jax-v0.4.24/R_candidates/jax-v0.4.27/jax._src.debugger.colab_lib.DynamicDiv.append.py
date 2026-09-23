  def append(self, child: DOMElement):
    if not self._rendered:
      self.render()
    with output.use_tags([self.tag]):
      with output.redirect_to_element(f"#{self.tag}"):
        child.render()
