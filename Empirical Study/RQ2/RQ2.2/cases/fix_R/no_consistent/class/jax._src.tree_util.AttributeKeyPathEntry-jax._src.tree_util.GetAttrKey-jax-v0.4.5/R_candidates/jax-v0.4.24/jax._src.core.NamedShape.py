class NamedShape:
  def __init__(self, *args, **kwargs):
    self.__positional = canonicalize_shape(args)
    # TODO: Assert that kwargs match axis env?
    self.__named = dict(kwargs)

  @property
  def rank(self):
    return len(self.__positional) + len(self.__named)

  @property
  def positional_rank(self):
    return len(self.__positional)

  @property
  def named_rank(self):
    return len(self.__named)

  @property
  def positional(self):
    return self.__positional

  @property
  def names(self):
    return self.__named.keys()

  @property
  def named_sizes(self):
    return self.__named.values()

  @property
  def named_items(self):
    return self.__named.items()

  def __getitem__(self, idx):
    try:
      idx = operator.index(idx)
      return self.__positional[idx]
    except TypeError:
      pass
    return self.__named[idx]

  @property
  def total(self):
    total = 1
    for s in self.__positional: total *= s
    for s in self.__named.values(): total *= s
    return total

  def __str__(self):
    # TODO(mattjj,frostig): revise not to miss commas
    if not self.__named:
      return str(self.__positional)
    return (f"({', '.join(map(str, self.__positional))}{', ' if self.__named else ''}"
            f"{', '.join(f'{k}={v}' for k, v in self.__named.items())})")

  def __eq__(self, other):
    if isinstance(other, NamedShape):
      return (self.__positional, self.__named) == (other.__positional, other.__named)
    if isinstance(other, tuple):
      return not self.__named and self.__positional == other
    return False

  def __hash__(self):
    named = frozenset(self.__named.items())
    return hash((self.__positional, named))
