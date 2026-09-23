class FlattenedKeyPathEntry(KeyPathEntry):  # fallback
  def pprint(self) -> str:
    return f'[<flat index {self.key}>]'
