@_wraps(np.isrealobj)
def isrealobj(x):
  return not iscomplexobj(x)
