@_wraps(np.frombuffer)
def frombuffer(buffer, dtype=float, count=-1, offset=0):
  return asarray(np.frombuffer(buffer=buffer, dtype=dtype, count=count, offset=offset))
