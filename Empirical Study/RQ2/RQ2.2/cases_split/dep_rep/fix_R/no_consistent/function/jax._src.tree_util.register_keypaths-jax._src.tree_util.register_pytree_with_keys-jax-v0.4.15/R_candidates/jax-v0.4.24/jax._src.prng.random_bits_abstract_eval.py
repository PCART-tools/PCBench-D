@random_bits_p.def_abstract_eval
def random_bits_abstract_eval(keys_aval, *, bit_width, shape):
  out_shape = (*keys_aval.shape, *shape)
  out_dtype = dtypes.dtype(f'uint{bit_width}')
  return core.ShapedArray(out_shape, out_dtype)
