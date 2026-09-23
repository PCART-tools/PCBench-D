def taggedtuple(name, fields) -> Callable[..., Any]:
  """Lightweight version of namedtuple where equality depends on the type."""
  def __new__(cls, *xs):
    return tuple.__new__(cls, (cls,) + xs)
  def __repr__(self):
    return f'{name}{tuple.__str__(self[1:])}'
  class_namespace = {'__new__' : __new__, '__repr__': __repr__}
  for i, f in enumerate(fields):
    class_namespace[f] = property(operator.itemgetter(i+1))  # type: ignore
  return type(name, (tuple,), class_namespace)
