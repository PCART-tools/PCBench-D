@util.implements(np.issubdtype)
def issubdtype(arg1: DTypeLike, arg2: DTypeLike) -> bool:
  return dtypes.issubdtype(arg1, arg2)
