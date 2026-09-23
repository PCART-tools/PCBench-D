class FrozenDict(abc.Mapping):
  def __init__(self, *args, **kwargs):
    self.contents = dict(*args, **kwargs)

  def __iter__(self):
    return iter(self.contents)

  def __len__(self):
    return len(self.contents)

  def __getitem__(self, name):
    return self.contents[name]

  def __eq__(self, other):
    return isinstance(other, FrozenDict) and self.contents == other.contents

  def __hash__(self):
    return hash(tuple(self.contents.items()))

  def __repr__(self):
    return f"FrozenDict({self.contents})"
