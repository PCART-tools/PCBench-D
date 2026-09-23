class ResourceCount(NamedTuple):
  nglobal: int
  nlocal: int | None
  distributed: bool

  def to_local(self, global_size):
    return global_size
