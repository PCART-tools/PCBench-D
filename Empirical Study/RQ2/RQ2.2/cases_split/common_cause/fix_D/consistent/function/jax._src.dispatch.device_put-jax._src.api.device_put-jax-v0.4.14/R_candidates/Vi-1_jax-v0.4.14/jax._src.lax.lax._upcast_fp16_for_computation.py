def _upcast_fp16_for_computation(f):
  @functools.wraps(f)
  def f_wrapped(x):
    dtype = _dtype(x)
    if dtype == np.float16 or dtype == dtypes.bfloat16:
      return convert_element_type(
        f(convert_element_type(x, np.float32)), dtype)
    return f(x)

  return f_wrapped
