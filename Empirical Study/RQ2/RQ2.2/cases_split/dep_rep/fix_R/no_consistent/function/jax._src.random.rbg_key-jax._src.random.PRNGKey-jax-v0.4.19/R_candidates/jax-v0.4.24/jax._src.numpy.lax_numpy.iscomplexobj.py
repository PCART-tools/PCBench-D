@util.implements(np.iscomplexobj)
def iscomplexobj(x: Any) -> bool:
  if x is None:
    return False
  try:
    typ = x.dtype.type
  except AttributeError:
    typ = asarray(x).dtype.type
  return issubdtype(typ, complexfloating)
