def key_array_constant_handler(x):
  arr = x.unsafe_raw_array()
  return mlir.get_constant_handler(type(arr))(arr)
