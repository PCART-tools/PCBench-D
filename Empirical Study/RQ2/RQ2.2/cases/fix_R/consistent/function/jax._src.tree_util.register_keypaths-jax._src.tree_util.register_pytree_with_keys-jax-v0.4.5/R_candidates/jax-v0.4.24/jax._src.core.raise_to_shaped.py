def raise_to_shaped(aval: AbstractValue, weak_type=None):
  aval_type = type(aval)
  if aval_type is ShapedArray and weak_type is None:
    return aval
  if weak_type is None:
    weak_type = getattr(aval, 'weak_type', False)
  for typ in aval_type.__mro__:
    handler = raise_to_shaped_mappings.get(typ)
    if handler: return handler(aval, weak_type)
  raise TypeError(type(aval))
