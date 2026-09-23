class AttributeKeyPathEntry(_DeprecatedKeyPathEntry):
  def pprint(self) -> str:
    return f'.{self.key}'
  def __str__(self):
    return self.pprint()
