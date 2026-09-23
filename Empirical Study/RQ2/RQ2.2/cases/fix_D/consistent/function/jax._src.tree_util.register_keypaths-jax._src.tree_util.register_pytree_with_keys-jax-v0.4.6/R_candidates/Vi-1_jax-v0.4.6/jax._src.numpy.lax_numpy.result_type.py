@util._wraps(np.result_type)
def result_type(*args: ArrayLike) -> DType:
  return dtypes.result_type(*args)
