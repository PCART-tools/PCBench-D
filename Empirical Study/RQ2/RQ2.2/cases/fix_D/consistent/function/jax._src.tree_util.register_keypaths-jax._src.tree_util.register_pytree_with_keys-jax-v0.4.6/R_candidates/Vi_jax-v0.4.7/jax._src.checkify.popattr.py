def popattr(obj, attrname):
  val = getattr(obj, attrname)
  delattr(obj, attrname)
  return val
