  def wrap_name(self, name: str) -> str:
    if not self.stack:
      return name
    return f'{self}/{name}'
