@util.implements(np.isrealobj)
def isrealobj(x: Any) -> bool:
  return not iscomplexobj(x)
