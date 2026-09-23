@util._wraps(np.frombuffer)
def frombuffer(buffer: bytes | Any, dtype: DTypeLike = float,
               count: int = -1, offset: int = 0) -> Array:
  return asarray(np.frombuffer(buffer=buffer, dtype=dtype, count=count, offset=offset))
