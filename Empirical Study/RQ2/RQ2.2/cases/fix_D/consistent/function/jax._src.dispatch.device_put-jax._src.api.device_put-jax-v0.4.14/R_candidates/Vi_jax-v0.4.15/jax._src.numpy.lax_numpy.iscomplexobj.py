@util._wraps(np.iscomplexobj)
def iscomplexobj(x: Any) -> bool:
  try:
    typ = x.dtype.type
  except AttributeError:
    typ = asarray(x).dtype.type
  return issubdtype(typ, complexfloating)
