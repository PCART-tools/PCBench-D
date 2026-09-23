def key_array_constant_handler(x):
  arr = x._base_array
  return mlir.get_constant_handler(type(arr))(arr)
