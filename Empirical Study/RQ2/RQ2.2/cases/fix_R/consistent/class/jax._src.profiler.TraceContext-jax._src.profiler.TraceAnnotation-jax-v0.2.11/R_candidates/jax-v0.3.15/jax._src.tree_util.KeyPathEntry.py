class KeyPathEntry(NamedTuple):
  key: Any
  def pprint(self) -> str:
    assert False  # must override
