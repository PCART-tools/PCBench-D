@iota_2x32_shape_p.def_abstract_eval
def iota_2x32_shape_abstract_eval(*, shape):
  return (core.ShapedArray(shape, np.dtype('uint32')),) * 2
