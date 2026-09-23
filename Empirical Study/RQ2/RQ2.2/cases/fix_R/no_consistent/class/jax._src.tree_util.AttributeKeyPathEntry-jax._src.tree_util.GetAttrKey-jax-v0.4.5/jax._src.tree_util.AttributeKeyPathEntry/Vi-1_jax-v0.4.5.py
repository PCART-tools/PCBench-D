class AttributeKeyPathEntry(KeyPathEntry):
  def pprint(self) -> str:
    return f'.{self.key}'
