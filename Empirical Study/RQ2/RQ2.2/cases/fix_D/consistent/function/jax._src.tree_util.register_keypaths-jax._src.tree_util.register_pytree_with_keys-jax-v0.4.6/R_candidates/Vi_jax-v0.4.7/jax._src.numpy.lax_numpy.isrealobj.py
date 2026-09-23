@util._wraps(np.isrealobj)
def isrealobj(x: Any) -> bool:
  return not iscomplexobj(x)
