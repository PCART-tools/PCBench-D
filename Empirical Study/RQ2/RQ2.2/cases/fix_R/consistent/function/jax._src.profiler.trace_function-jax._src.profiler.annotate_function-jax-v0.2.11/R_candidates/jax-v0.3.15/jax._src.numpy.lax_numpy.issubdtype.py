@_wraps(np.issubdtype)
def issubdtype(arg1, arg2):
  return dtypes.issubdtype(arg1, arg2)
