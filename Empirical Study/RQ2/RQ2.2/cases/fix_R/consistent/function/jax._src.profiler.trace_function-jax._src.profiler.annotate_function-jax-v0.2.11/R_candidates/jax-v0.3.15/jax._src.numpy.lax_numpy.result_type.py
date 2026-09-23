@_wraps(np.result_type)
def result_type(*args):
  return dtypes.result_type(*args)
