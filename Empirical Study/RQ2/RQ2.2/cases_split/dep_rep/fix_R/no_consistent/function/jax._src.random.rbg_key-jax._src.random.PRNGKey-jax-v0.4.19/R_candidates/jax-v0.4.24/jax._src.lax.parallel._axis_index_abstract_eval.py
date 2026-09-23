def _axis_index_abstract_eval(*, axis_name):
  frame = core.axis_frame(axis_name)
  return ShapedArray((), np.int32, named_shape={axis_name: frame.size})
