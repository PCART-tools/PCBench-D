class GetitemKeyPathEntry(KeyPathEntry):
  def pprint(self) -> str:
    return f'[{repr(self.key)}]'
